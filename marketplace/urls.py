from django.urls import path
from .views import CategoryView
app_name = 'marketplace'

urlpatterns = [
    path('category/',CategoryView.as_view(),name='category')
]
