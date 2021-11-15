from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.core.paginator import Paginator

class CategoryView(View):
    def get(self, request, *args, **kwargs):
       
        context = {
        }
        return render(request, 'pages/products/categories.html', context)
    
class InfoView(View):
    def get(self, request, *args, **kwargs):
       
        context = {
        }
        return render(request, 'pages/info.html', context)