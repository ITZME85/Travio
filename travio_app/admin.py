from django.contrib import admin
from django.utils.html import format_html
from .models import*

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ('company_name','name','email','contact_number','password')
    

class TourPics(admin.TabularInline):
    model = AddPhotos
    extra=0
    readonly_fields = ['preview']
    def preview(self,obj):
        return format_html('<img src="{}" width="100" />',obj.image.url)
    
@admin.register(TourPackage)
class ListAdmin(admin.ModelAdmin):
    list_display = ('package_name','price')
    list_filter = ('is_approved',)
    inlines = [TourPics]
    readonly_fields = ['created_at']
    actions = ['approve_selected']
    def approve_selected(self,request,queryset):
        queryset.update(is_approved = True) 
    approve_selected.short_description = "Approve selected tour package"


# admin.site.register(vendorRegister)
admin.site.register(vendorRegister,VendorAdmin)
# admin.site.register(TourPics,ListAdmin)