from django.contrib import admin

# Register your models here.
from .models import Property  # Tumhare model ka naam

from django.contrib import admin
from .models import Property,User

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'agency_name', 'agency_product', 'area', 'bathroom', 'bedroom',
        'category', 'city', 'contact_name', 'property_id', 'latitude',
        'longitude', 'location', 'occupancy_status', 'ownership_status',
        'price', 'primary_image', 'primary_mobile_no', 'primary_phone_no',
        'primary_video', 'product', 'product_score', 'property_tour',
        'purpose', 'short_description', 'state', 'title', 'whatsapp_no','user'
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'role', 'username', 'email'
    )
