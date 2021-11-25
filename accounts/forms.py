from django.db.models.fields import Field
from accounts.models import User, UserPayment
from django import forms
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime
from calendar import monthrange


MM_OPTIONS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
)

AA_OPTIONS = (
    ('2021', '2221'),
    ('2222', '2222'),
    ('2223', '2223'),
    ('2224', '2224'),
    ('2225', '2225'),
    ('2226', '2226'),
    ('2227', '2227'),
    ('2228', '2228'),
)


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
    card = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text",
        'class': "block w-full px-5 py-2 border rounded-lg bg-white shadow-lg placeholder-gray-400 text-gray-700 focus:ring focus:outline-none",
        'placeholder': "Número de tarjeta",
        'maxlength': "19",
        'x-model': "cardNumber",
        
        'x-on:keydown':'format()',
        'x-on:keyup':'isValid()'

    }), required=True)
    owner_of_card = forms.CharField(widget=forms.TextInput(attrs={
        
        'type': "text",
        'class': "block w-full px-5 py-2 border rounded-lg bg-white shadow-lg placeholder-gray-400 text-gray-700 focus:ring focus:outline-none",
        'placeholder': "Nombre de la tarjeta",
        'maxlength': "22",
        'x-model': "cardholder"

    }), required=True)
    csv_filename = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text",
        'class': "block w-full col-span-2 px-5 py-2 border rounded-lg bg-white shadow-lg placeholder-gray-400 text-gray-700 focus:ring focus:outline-none",
        'placeholder': "CVC",
        'maxlength': "3",
        'x-model': "securityCode",
        'x-on:focus': "card = 'back'",
        'x-on:blur': "card = 'front'"

    }), required=True)
    dateMM = forms.ChoiceField(required=True, widget=forms.Select(attrs={
        'class': "form-select appearance-none block w-full px-5 py-2 border rounded-lg bg-white shadow-lg placeholder-gray-400 text-gray-700 focus:ring focus:outline-none",
        'x-model': "expired.month",
    }), choices=MM_OPTIONS)
    
    dateAA = forms.ChoiceField(required=True, widget=forms.Select(attrs={
        'class': "form-select appearance-none block w-full px-5 py-2 border rounded-lg bg-white shadow-lg placeholder-gray-400 text-gray-700 focus:ring focus:outline-none",
        'x-model': "expired.year",
    }), choices=AA_OPTIONS)
    
    class Meta:
        model = UserPayment
        fields = ('card', 'csv_filename', 'owner_of_card','dateMM','dateAA')
