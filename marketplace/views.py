from django.shortcuts import render, redirect, get_object_or_404
from .models import Categories,Product
from django.views import View
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count
from django.db.models import Q
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        if query=="TODAS":
            category_list = Product.objects.filter(active=True)
        else:
            category_list = Product.objects.filter(Q(category__name=query))
        page =request.GET.get('page',1)
        paginator =Paginator(category_list,6)
        try:
            categories_list=paginator.page(page)
        except PageNotAnInteger:
            categories_list = paginator.page(1)
        except EmptyPage:
            categories_list = paginator.page(paginator.num_pages)
        categories = Categories.objects.all()
       
        
        context = {
            'categories_list': categories_list,
            'query': query,
            'categories':categories,
        }
        return render(request, 'pages/products/categories.html', context)
    
class InfoView(View):
    def get(self, request, *args, **kwargs):
       
        context = {
        }
        return render(request, 'pages/info.html', context)