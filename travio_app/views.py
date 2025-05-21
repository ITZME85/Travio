from django.shortcuts import render,redirect,get_object_or_404
from .forms import*
from django.contrib.auth import authenticate,login,logout,get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.urls import reverse
from django.contrib import messages


# Create your views here.
# @login_required(login_url='user_login/')

def index(request):
    return render (request,'index.html')

def vendor_reg(request):
    error_message = None
    if request.method == 'POST':
       form=vendorRegisterForm(request.POST)
       if form.is_valid():
        username = form.cleaned_data.get('company_name')
        password = form.cleaned_data.get('password')
        password2=form.cleaned_data.get('password2')
        hashed = make_password(password)
        if vendorRegister.objects.filter(company_name=username):
            error_message = ' Company name already exists'
            return render(request,'vendor_reg.html',{'form':form,'error':error_message})
        else:
            if password2 != password:
               error_message = "Passwords doesn't match"
               return render(request,'vendor_reg.html',{'form':form,'pass_error':error_message})
            else:
                user = form.save(commit=False)
                user.password = hashed
                user.save()
                return redirect('vendor_log')     
    else:
        form=vendorRegisterForm
    return render(request,'vendor_reg.html',{'form':form})

def vendor_log(request):
   error_message = None
   if request.method == "POST":
      form = VendorLoginForm(request.POST)
      if form.is_valid():
         username = form.cleaned_data.get("company_name")
         password = form.cleaned_data.get('password')
         try:
            vendor = vendorRegister.objects.get(company_name=username)
            if check_password(password,vendor.password):
            #  login(request,vendor)
             request.session['vendor_id']=vendor.id
             return redirect('vendor')
         except:
            error_message = 'Invalid company name or password'
            return render(request,'vendor_log.html',{'form':form,'error_message':error_message})

   else:
        form = VendorLoginForm
   return render(request,'vendor_log.html',{'form':form})

def register(request):
    if request.method == 'POST':
      form = RegistraionForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('index')
    else:
      form = RegistraionForm
    return render(request,'user_reg.html',{'form':form})

def Userlogin(request):
    error_message = None
    if request.method == 'POST':
       form = LogInForm(request.POST)
       if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        # user.is_active = True
        if user is not None:
            login(request,user)
            return redirect('user')
        else:
            error_message = 'invalid username or password'
            return render(request,'user_log.html',{'form':form,'error_message':error_message})
        
    form = LogInForm
    return render(request,'user_log.html',{'form':form})

def log_out(request):
   logout(request)
#    return HttpResponse("You are logged out")
   return redirect('user_log')

def usr(request):
   # bookings = booking.objects.filter(user = request.user).select_related('package')
   return render(request,'user.html',{'user':request.user})

# @login_required(login_url='vendor_login/')
def vendor_dash(request):
      vendor_id = request.session.get('vendor_id')
     
      vendor = vendorRegister.objects.get(id=vendor_id)
      list = TourPackage.objects.filter(vendor=vendor)
      return render(request,'vendor.html',{'vendor':vendor,'list':list})

def vendor_logout(request):
   logout(request)
   return redirect('vendor_log')


def add_package(request):
   vendor_id = request.session.get('vendor_id')
   if not vendor_id:
      return redirect('vendor_log')
   vendor = vendorRegister.objects.get(id=vendor_id)
   if request.method == 'POST':
    #   form = TourPackageForm(request.POST,request.FILES.getlist('photos'))
    #   if form.is_valid():
    #      tour_package=form.save(commit=False)
    #      tour_package.vendor=vendorRegister.objects.get(id=request.session['vendor_id'])
    #      form.save()
        package_name = request.POST['package_name']
        destinations = request.POST['destinations']
        price = request.POST['price']
        images = request.FILES.getlist('photos')
        package = TourPackage.objects.create(vendor=vendor,package_name=package_name,price=price,destinations=destinations)
        for img in images:
           AddPhotos.objects.create(package=package,image=img)
        return  redirect('vendor')
   else:
      form = TourPackageForm()
      return render (request,'upload.html',{'form':form})
   
def packages(request):
   packs = TourPackage.objects.filter(is_approved=True)
   return render(request,'tour_packages.html',{'packages':packs})


# @login_required(login_url='user_log')
def payment_page(request):
      package_id = request.session.get('package_id')
      if not package_id:
         return redirect('some_error_on_package_list')
      package = get_object_or_404(TourPackage,id=package_id)
      return render(request,'payment_page.html',{'package':package})

def book(request,package_id):
   if not request.user.is_authenticated:
      return redirect('user_log')
   request.session['package_id'] = package_id
   return redirect('payment_page')