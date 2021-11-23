from django.db import models
from django.contrib.auth.models import AbstractUser
from marketplace.models import Product,PurchasedProduct
from django.db.models.signals import post_save
import os
from django.conf import settings

def user_directory_path_profile(instance,filename):
    profile_picture_name ='users/{0}/profile.jpg'.format(instance.username)
    full_path= os.path.join(settings.MEDIA_ROOT,profile_picture_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_picture_name

VERIFICATION_OPTIONS=(
    ('unverified','unverified'),
    ('verified','verified'),
)

class User(AbstractUser):
    stripe_customer_id=models.CharField(max_length=50,null=True, blank=True)
    photo=models.ImageField(default='users/user_default_bg.png',upload_to=user_directory_path_profile)
    created=models.DateTimeField(auto_now_add=True)
    verifield=models.CharField(max_length=10,choices=VERIFICATION_OPTIONS,default='unverified')
    coins  =models.DecimalField(max_digits=19,decimal_places=2,default=0,blank=False)  
    date_created =models.DateField(auto_now_add=True)
    def get_produsts_count(self):
        return self.library.products.all().count()
    
    def get_produsts_count_public(self):
        return self.products.all().count()
    
class UserPayment(models.Model):
    card=models.IntegerField(null=False)
    expired=models.DateField(auto_now_add=False,null=False)
    csv_filename= models.IntegerField(null=False)
    owner_of_card=models.CharField(max_length=80,null=False)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="payment")
    
    def __str__(self):
        return self.user.email

class UserLibraty(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="library")
    products=models.ManyToManyField(Product, blank=True)
    def __str__(self):
        return self.user.email
    
    
    

def post_save_user_receiver(sender,instance,created,**kwargs):
    if created:
        library=UserLibraty.objects.create(user=instance)
        purchased_products=PurchasedProduct.objects.filter(email=instance.email)
        
        for purchased_product in purchased_products:
            library.products.add(purchased_product.product)
            
post_save.connect(post_save_user_receiver,sender=User)

