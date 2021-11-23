from django.urls import path
from .views import EditProfile,AddPaymentView
app_name='accounts'

urlpatterns =[
    path('profile/edit', EditProfile, name="edit-profile"),
    path('payment/', AddPaymentView.as_view(), name="add-payment"),
]