from django.db import models
from RealEstateApp.models import User
from RealEstateApp.models import Property

class Inquiry(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20,default='Pending', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Declined', 'Declined')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
