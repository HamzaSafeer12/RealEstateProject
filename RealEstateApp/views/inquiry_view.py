from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from RealEstateApp.models import Inquiry , Notification, User
from RealEstateApp.serializer import InquirySerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model

class InquiryView(APIView):
     def post(self, request):
          serializer = InquirySerializer(data=request.data)
          if serializer.is_valid():
               inquiry = serializer.save(buyer=request.user)  # Save inquiry and associate it with the logged-in user

               # Send notification to admins
               admin_users = User.objects.filter(role='Admin')  # Assuming `role` is used to distinguish admin users
               for admin in admin_users:
                    Notification.objects.create(admin=admin, inquiry=inquiry)  # Save notification for each admin

               return Response(serializer.data, status=status.HTTP_201_CREATED)
          
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
