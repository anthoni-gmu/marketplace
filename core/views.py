from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic.base import TemplateView
from marketplace.models import Product, PurchasedProduct,Reviews
from marketplace.forms import ProductModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.conf import settings
import stripe
from stripe.error import SignatureVerificationError
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.models import UserLibraty
stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(active=True)
        form = ProductModelForm()
        
        
        page =request.GET.get('page',1)
        paginator =Paginator(products,6)

        try:
            productsActivated=paginator.page(page)
        except PageNotAnInteger:
            productsActivated = paginator.page(1)
        except EmptyPage:
            productsActivated = paginator.page(paginator.num_pages)
        
        
        context = {
            'products': productsActivated,
            'form': form
        }
        return render(request, 'pages/index.html', context)

    def post(self, request, *args, **kwargs):
        products = Product.objects.filter(active=True)

        form = ProductModelForm()

        if request.method == "POST":
            form = ProductModelForm(request.POST, request.FILES)

            if form.is_valid():
                form.user = request.user
                name = form.cleaned_data.get('name')
                description = form.cleaned_data.get('description')
                thumbnail = form.cleaned_data.get('thumbnail')
                slug = form.cleaned_data.get('slug')
                content_file = form.cleaned_data.get('content_file')
                price = form.cleaned_data.get('price')
                active = form.cleaned_data.get('active')
                category = form.cleaned_data.get('category')
                p, created = Product.objects.get_or_create(user=form.user, name=name, description=description, thumbnail=thumbnail,
                
                                                           slug=slug, content_file=content_file, price=price, active=active)
                for cat in category:
                    p.category.add(cat)
                p.category.all()
                p.save()
                return redirect('home')

        digital_products_data = None

        if products:
            paginator = Paginator(products, 9)
            page_number = request.GET.get('page')
            digital_products_data = paginator.get_page(page_number)

        context = {
            'products': digital_products_data
        }
        return render(request, 'pages/index.html', context)


class UserProductList(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(user=request.user)
        
        

        context = {
            'products': products
        }
        return render(request, 'pages/products/user_productlist.html', context)

class UserLibraryView(LoginRequiredMixin,View):
    def get(self, request,username, *args, **kwargs):
        user=get_object_or_404(User,username=username)
        userlibrary=UserLibraty.objects.get(user=user)
        context={
            'userlibrary':userlibrary
        }
        
        return render(request, 'pages/products/library.html', context)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'pages/products/edit.html'
    form_class = ProductModelForm

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('product-list')


class ProdutDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        product = get_object_or_404(Product, slug=slug)
        has_access = None
        if self.request.user.is_authenticated:
            if product in self.request.user.library.products.all():
                has_access=True
        
        context = {
            'product': product,

        }
        context.update({
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            'has_access': has_access
            
        })
        return render(request, 'pages/products/detail.html', context)


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(slug=self.kwargs['slug'])

        domain = "www.mrtoni.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        customer=None
        customer_email =None   
        if request.user.is_authenticated:
            if request.user.stripe_customer_id:
                customer=request.user.stripe_customer_id
            else:
                customer_email=request.user.email
        session = stripe.checkout.Session.create(
            customer=customer, 
            customer_email=customer_email,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': product.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + reverse('success'),
            cancel_url=domain + reverse('home'),
            metadata={
                "product_id":product.id
            }
        )
        return JsonResponse({
            "id": session.id
        })

class SuccesVies(TemplateView):
    template_name = 'pages/products/success.html'
    
    
@csrf_exempt
def stripe_webhook(request, *args, **kwargs):
    CHECKOUT_SESSION_COMPLETED="checkout.session.completed"
    payload = request.body
    
    sig_header=request.META.get('HTTP_STRIPE_SIGNATURE')
    try:
        event = stripe.Webhook.construct_event(
        payload,
        sig_header, 
        settings.STRIPE_WEBHOOK_SECRET

    )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    
    except SignatureVerificationError as e:
        print(e)
        return HttpResponse(status=400)
    print(event)
    if event["type"] == CHECKOUT_SESSION_COMPLETED:
        print(event)
        product_id=event["data"]["object"]["metadata"]["product_id"]
        product=Product.objects.get(id=product_id)
        
        stripe_customer_id=event["data"]["object"]["customer"]
        try:
            #revisar si el usuario ya tiene un customer ID
            user = User.objects.get(stripe_customer_id=stripe_customer_id)

            user.library.products.add(product)
            user.library.save()

        except User.DoesNotExist:
            #si el usuario no tiene customer ID, pero este si esta registrado en el sitio web
            stripe_customer_email = event["data"]["object"]["customer_details"]["email"]
            try:
                user = User.objects.get(email=stripe_customer_email)
                user.stripe_customer_id = stripe_customer_id
                user.library.products.add(product)
                user.library.save()

            except User.DoesNotExist:
                PurchasedProduct.objects.create(
                    email=stripe_customer_email,
                    product=product
                )

                send_mail(
                    subject="Create an account to access your content",
                    message="Please signup to access your products",
                    recipient_list=[stripe_customer_email],
                    from_email="Vudera <mail@vudera.com>"
                )

                pass


    # pagos exitosos

    # quien pago por que cosa?

    # dar acceso al production

    return HttpResponse()
