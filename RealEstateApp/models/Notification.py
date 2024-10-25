from django.db import models
from RealEstateApp.models import User, Inquiry

class Notification(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
