from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class vendorRegister(models.Model):
    name = models.CharField(max_length=100,blank=False)
    company_name = models.CharField(max_length=20,blank=False)
    email = models.EmailField(max_length=200)
    contact_number = PhoneNumberField(unique=True,region='IN')
    password = models.CharField(max_length=200)


class TourPackage(models.Model):
    vendor = models.ForeignKey(vendorRegister,on_delete=models.CASCADE)
    package_name = models.CharField(max_length=100,blank=False)
    destinations = models.CharField(max_length=100,blank=False)
    price = models.DecimalField(max_digits=10,decimal_places=0)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class AddPhotos(models.Model):
    package = models.ForeignKey(TourPackage,on_delete=models.CASCADE,related_name='photos')
    image = models.ImageField(upload_to='tour_pics/')
    created_at = models.DateTimeField(auto_now_add=True)






