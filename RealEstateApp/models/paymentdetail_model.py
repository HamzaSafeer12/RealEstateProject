from django.db import models
from RealEstateApp.models import User
from RealEstateApp.models import Property

class PaymentDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User ID
    property = models.ForeignKey(Property, on_delete=models.CASCADE)  # Property ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    charge_id = models.CharField(max_length=100, unique=True)  # Stripe charge ID
    created_at = models.DateTimeField(auto_now_add=True)  # Payment timestamp
