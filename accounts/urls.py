from django.urls import path
from .views import EditProfile,AddPaymentView,EditPayment
app_name='accounts'

urlpatterns =[
    path('profile/edit', EditProfile, name="edit-profile"),
    path('payment/', AddPaymentView.as_view(), name="add-payment"),
    path('edit/<pk>', EditPayment, name="edit-payment"),
    
]