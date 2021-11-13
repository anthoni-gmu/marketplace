from django.contrib import admin

# Register your models here.
from .models import UserLibraty,User,UserPayment

admin.site.register(User)
admin.site.register(UserLibraty)
admin.site.register(UserPayment)
