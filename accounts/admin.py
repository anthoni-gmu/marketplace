from django.contrib import admin

# Register your models here.
from .models import UserLibraty,User

admin.site.register(User)
admin.site.register(UserLibraty)
