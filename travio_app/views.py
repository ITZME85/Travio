from django.shortcuts import render,redirect,get_object_or_404
import razorpay.errors
from .forms import*
from django.contrib.auth import authenticate,login,logout,get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))


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
    next_url = request.session.get('next', 'user')

    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Clear the session
                if 'next' in request.session:
                    next_url = request.session.pop('next')
                return redirect(next_url)
            else:
                error_message = 'Invalid username or password'
                return render(request, 'user_log.html', {'form': form, 'error_message': error_message})
    
    form = LogInForm
    return render(request, 'user_log.html', {'form': form})

def log_out(request):
   logout(request)
#    return HttpResponse("You are logged out")
   return redirect('user_log')



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
        description = request.POST['description']
        price = request.POST['price']
        images = request.FILES.getlist('photos')
        package = TourPackage.objects.create(vendor=vendor,package_name=package_name,price=price,description=description)
        for img in images:
           AddPhotos.objects.create(package=package,image=img)
        return  redirect('vendor')
   else:
      form = TourPackageForm()
      return render (request,'upload.html',{'form':form})
   
def packages(request):
   packs = TourPackage.objects.filter(is_approved=True)
   return render(request,'tour_packages.html',{'packages':packs})


@login_required(login_url='user_log')
def payment(request, package_id):
    try:
        package = get_object_or_404(TourPackage, id=package_id, is_approved=True)  
        existing_order = Order.objects.filter(
            user=request.user,
            package=package,
            status='Pending'
        ).first()
        
        if existing_order:
            order = existing_order
        else:
            
            order = Order.objects.create(
                user=request.user,
                package=package,
                status='Pending'
            )
            
            
            razorpay_order = client.order.create({
                "amount": int(package.price * 100),  
                "currency": "INR",
                "payment_capture": 1,
                "notes": {
                    "package_name": package.package_name,
                    "user_email": request.user.email
                }
            })
            
            order.razorpay_order_id = razorpay_order['id']
            order.save()

        context = {
            "package": package,
            "order": order,
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": order.razorpay_order_id,
            "amount": int(package.price * 100),
            "user": request.user,
            "callback_url": request.build_absolute_uri(reverse('payment_success'))
        }
        
        return render(request, 'payment_page.html', context)
        
    except Exception as e:
        return redirect('payment_failed')

# @login_required(login_url='user_log')
@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')

            
            order = get_object_or_404(Order, razorpay_order_id=order_id)

            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            order.razorpay_payment_id = payment_id
            order.razorpay_signature = signature
            order.status = 'Paid'
            order.save()

            return render(request, 'payment_success.html', {'order': order})
            
        except Exception as e:
            print(f"Payment Success Error: {str(e)}")
            return redirect('payment_failed')
            
    return HttpResponseBadRequest()

# @login_required(login_url='user_log')
def payment_failed(request):
    context = {
        'error_message': request.GET.get('error', 'Transaction failed. Please try again.')
    }
    return render(request, 'payment_failed.html', context)

def contact(request):
    if request.method == 'POST':
        # Add your email sending logic here
        return redirect('index')
    return render(request, 'contact.html')

@login_required(login_url='user_log')
def user_dashboard(request):
    if request.user.is_authenticated:
        # Get user's bookings
        bookings = Order.objects.filter(
            user=request.user
        ).select_related('package').prefetch_related('package__photos')

        # Get user's stats
        total_bookings = bookings.count()
        total_places = bookings.values('package__description').distinct().count()
        
        context = {
            'user': request.user,
            'bookings': bookings,
            'total_bookings': total_bookings,
            'total_places': total_places
        }
        return render(request, 'user.html', context)
    return redirect('user_log')

# def usr(request):
#    bookings = Order.objects.filter(user = request.user).select_related('package')
#    return render(request,'user.html',{'user':request.user})