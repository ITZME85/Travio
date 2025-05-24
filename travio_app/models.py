from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
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
    description = models.TextField()  # Changed from destinations
    price = models.DecimalField(max_digits=10,decimal_places=2)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class AddPhotos(models.Model):
    package = models.ForeignKey(TourPackage,on_delete=models.CASCADE,related_name='photos')
    image = models.ImageField(upload_to='tour_pics/')
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage,on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=1000)
    razorpay_payment_id = models.CharField(max_length=1000)
    razorpay_signature = models.CharField(max_length=1000)
    status = models.CharField(max_length=100,default='created')
    booked_at = models.DateTimeField(auto_now_add=True)






