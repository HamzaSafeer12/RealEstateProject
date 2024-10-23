from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from RealEstateApp.models import User
from rest_framework.decorators import api_view
from RealEstateApp.serializer import UserSerializer
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST['role']

        encoded_password = make_password(password)

        user_data = {
            'username': username,
            'email': email,
            'password': encoded_password,
            'role': role
        }

        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_login')
        else:
            print(serializer.errors)
        

    return render(request, 'user_signup.html')
