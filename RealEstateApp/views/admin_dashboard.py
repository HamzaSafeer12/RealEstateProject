from django.shortcuts import render

def AdminDashboard(request):
    return render(request, 'admin_dashboard.html')