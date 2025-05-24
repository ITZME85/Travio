from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User


class vendorRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create Password',
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })
    )
    class Meta:
        model = vendorRegister
        fields = ['name', 'company_name', 'email', 'contact_number', 'password', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Full Name',
                'class': 'form-control'
            }),
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Company Name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control'
            }),
            'contact_number': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'form-control'
            })
        }


class VendorLoginForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    class Meta:
        model = vendorRegister
        fields = ['company_name', 'password']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name'})
        }


# #Authentication
# class SigninForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['username','password']


#UserCreation

class RegistraionForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

#Authentication
class LogInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ['package_name', 'description', 'price']  # Changed from destinations
        widgets = {
            'package_name': forms.TextInput(attrs={
                'placeholder': 'Package Name',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={  # Changed from destinations
                'placeholder': 'Package Description',
                'class': 'form-control',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Price',
                'class': 'form-control'
            })
        }