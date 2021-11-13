from django.db import models
import os
from django.conf import settings
User=settings.AUTH_USER_MODEL


def marketplace_directory_path(instance,filname):
    banner_pic_name='marketplace/products/{0}/{1}'.format(instance.name,filname)
    full_path = os.path.join(settings.MEDIA_ROOT,banner_pic_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)
    return banner_pic_name


class Categories(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='products')
    name=models.CharField(max_length=100)
    description=models.TextField()
    thumbnail=models.ImageField(blank=True,null=True,upload_to=marketplace_directory_path)
    slug=models.SlugField(unique=True)
    content_url=models.URLField(blank=True,null=True)
    content_file=models.FileField(blank=True,null=True)
    ##content_file = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    active=models.BooleanField(default=False)
    
    price=models.PositiveIntegerField(default=100)
    category = models.ManyToManyField(Categories)
    def __str__(self):
        return self.name
    
    def price_display(self):
        return "{0:.2f}".format(self.price/100)


   
class PurchasedProduct(models.Model):
    email=models.EmailField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date_purchased=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email