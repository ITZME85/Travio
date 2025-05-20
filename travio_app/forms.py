from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User


class vendorRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = vendorRegister
        fields = ['name','company_name','email','contact_number','password','password2']
        

class VendorLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = vendorRegister
        fields = ['company_name','password']
        

# #Authentication
# class SigninForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['username','password']


#UserCreation

class RegistraionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']

#Authentication
class LogInForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ['package_name','destinations','price']