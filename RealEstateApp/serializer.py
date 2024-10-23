from RealEstateApp.models import User
from .models import Property
from .models import DummyModel
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # is trah hm khali name ko serilize kr sakhty hain means k name khali json ki form ma aye ga
        # fields=['name']
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'  # Ya specific fields ka list
class DummyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyModel
        fields = '__all__'
