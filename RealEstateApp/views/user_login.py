import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.shortcuts import render
from RealEstateApp.models import User
from django.shortcuts import render
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from RealEstateApp.task import send_password_reset_email

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Authenticate the user
#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             # If authentication is successful, log the user in
#             auth_login(request, user)
#             if user.role == 'admin':
#                 return redirect('AdminDashboard')
#             elif user.role == 'agent':
#                 return redirect('AgentDashboard')
#             else:
#                 return redirect('buyerDashboard')
#         else:
#             # If authentication fails, show an error message
#             return render(request, 'user_login.html', {'error': 'Invalid email or password'})
    # If it's a GET request, just render the login form
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)
        else:
            return Response({'error': 'Invalid email or password'}, status=400)


    def get(self, request):
        return render(request, 'user_login.html')
    

class PasswordResetRequest(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            
            reset_pin = str(random.randint(100000, 999999))
            user.reset_pin = reset_pin
            user.save()

            subject = 'Password Reset Request'
            message = f'Your password reset PIN is: {reset_pin}'
            recipient_list = [email]

            # Yahan Celery task ko background mein run kar rahe hain
            send_password_reset_email.delay(subject, message, recipient_list)

            return Response({"message": "Reset pin has been sent to your email."}, status=200)

        except User.DoesNotExist:
            return Response({"error": "This email is not registered."}, status=404)



class PasswordReset(APIView):
    def post(self, request):
        email = request.data.get('email')
        reset_pin = request.data.get('reset_pin')
        new_password = request.data.get('new_password')
        
        try:
            user = User.objects.get(email=email, reset_pin=reset_pin)
            
            # Reset the password
            user.set_password(new_password)
            user.reset_pin = None  # Optional: Clear the pin after successful reset
            user.save()
            
            return Response({"message": "Password has been reset successfully."}, status=200)

        except User.DoesNotExist:
            return Response({"error": "Invalid pin or email."}, status=400)



