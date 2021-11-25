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
        user=request.user.id 
        payment=UserPayment.DoesNotExist()
        form=AddPaymentForm(request.POST)
        
        if form.is_valid():
            print("ecoooooooss")
            
            new_comment=form.save(commit=False)
            new_comment.user=request.user
            new_comment.save() 
            
        else:
            print(form.non_field_errors)
        context={
            'form':form,
        }
        
        return render(request,'pages/users/add_payment.html',context)