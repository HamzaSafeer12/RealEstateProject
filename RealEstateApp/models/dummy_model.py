from django.db import models
from RealEstateApp.models import User

class DummyModel(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)