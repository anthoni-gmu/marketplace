from django.db.models.fields import Field
from accounts.models import User, UserPayment
from django import forms
from django.contrib.auth.models import AbstractUser


class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline',
        'placeholder': 'Nombre'
    }), required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline',
            'placeholder': 'Apellido'
        }), required=False
    )
    photo = forms.ImageField(label='Foto de perfil', required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline '
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'photo',)


class AddPaymentForm(forms.ModelForm):
    
    class Meta:
        model = UserPayment
        fields = ('card',  'expired', 'csv_filename','owner_of_card',)
