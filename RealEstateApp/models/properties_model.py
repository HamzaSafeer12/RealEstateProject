from django.db import models
from RealEstateApp.models import User

class Property(models.Model):
    agency_name = models.CharField(max_length=255)
    agency_product = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    bathroom = models.IntegerField()
    bedroom = models.IntegerField()
    category = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=255)
    property_id = models.AutoField(primary_key=True)  # 'id' ko property_id ka naam diya hai
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location = models.CharField(max_length=255)
    occupancy_status = models.CharField(max_length=50, default="notSpecified")
    ownership_status = models.CharField(max_length=50, default="notSpecified")
    price = models.CharField(max_length=50)
    primary_image = models.ImageField(upload_to='images/')
    primary_mobile_no = models.CharField(max_length=20)
    primary_phone_no = models.CharField(max_length=20)
    primary_video = models.URLField(max_length=500, blank=True, null=True)
    product = models.CharField(max_length=100)
    product_score = models.CharField(max_length=10)
    property_tour = models.URLField(max_length=500, blank=True, null=True)
    purpose = models.CharField(max_length=50)
    short_description = models.TextField()
    state = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    whatsapp_no = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
