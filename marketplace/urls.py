from django.urls import path
from .views import CategoryView,InfoView
app_name = 'marketplace'

urlpatterns = [
    path('post/search/category/', CategoryView.as_view(), name='category'),
    path('info/',InfoView.as_view(),name='info'),
]
