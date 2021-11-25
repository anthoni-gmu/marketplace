from django.shortcuts import render
from .models import User,UserPayment
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm,AddPaymentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
@login_required
def EditProfile(request):
    user =request.user.id 
    profile=User.objects.get(id=user)
    user_basic_info=User.objects.get(id=user)
    if request.method == 'POST':
        form=EditProfileForm(request.POST,request.FILES,instance=profile)
        
        if form.is_valid():
            user_basic_info.first_name=form.cleaned_data.get('first_name')
            user_basic_info.last_name=form.cleaned_data.get('last_name')
            profile.photo=form.cleaned_data.get('photo')
            profile.save()
            user_basic_info.save()
            return redirect('home')
    else:
        form=EditProfileForm(instance=profile)
    context={
        'form':form,
    }
    return render(request, 'pages/users/edit.html', context)
    
class AddPaymentView(View):
    def get(self, request, *args, **kwargs):
        form=AddPaymentForm()
        
        context = {
            'form':form,
        }
        return render(request, 'pages/users/add_payment.html', context)
    
    def post(self,request, *args, **kwargs):
        form=AddPaymentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user=request.user
            new_comment.save() 
        
        return redirect('home')

@login_required
def EditPayment(request, pk):
    user = request.user.id
    logged_in_user = request.user
    payment = UserPayment.objects.get(pk=pk)

    if request.method == 'POST':
        form = AddPaymentForm(request.POST,  instance=payment)
        if form.is_valid():
            payment.card = form.cleaned_data.get('card')
            payment.dateMM = form.cleaned_data.get('dateMM')
            payment.dateAA = form.cleaned_data.get('dateAA')
            payment.csv_filename = form.cleaned_data.get('csv_filename')
            payment.owner_of_card = form.cleaned_data.get('owner_of_card')

            payment.save()
            return redirect('home')
        else:
            return redirect('home')
    else:
        payment = UserPayment.objects.get(pk=pk)
        form = AddPaymentForm(instance=payment)

    context = {
        'form': form,
        'payment': payment
    }
    return render(request, 'pages/users/edit-payment.html', context)