from django.urls import path
from .views import EditProfile
app_name='accounts'

urlpatterns =[
    path('profile/edit', EditProfile, name="edit-profile"),
]