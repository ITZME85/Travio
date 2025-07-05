from django.urls import path
from .import views as v
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',v.index,name='index'),
    path('vendor_register/',v.vendor_reg,name='vendor_reg'),
    path('vendor_login/',v.vendor_log,name='vendor_log'),
    path('user_register/',v.register,name='user_reg'),
    path('user_login/',v.Userlogin,name='user_log'),
    path('user_logout/',v.log_out,name='user_out'),
    path('vendor_logout/',v.vendor_logout,name='vendor_out'),
    path('user/dash',v.user_dashboard,name='user'),
    path('vendor/',v.vendor_dash,name='vendor'),
    path('add_packages/',v.add_package,name='add'),
    path('packages/',v.packages,name='packages'),
    path('payment_page/<int:package_id>/',v.payment,name='payment_page'),
    path('payment/success/',v.payment_success,name='payment_success'),
    path('payment/failed/', v.payment_failed, name='payment_failed'),
    path('contact/', v.contact, name='contact'),
    path('list<int:pk>/delete',v.delete,name='delete'),
    path('list<int:pk>/edit',v.edit,name='edit'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)