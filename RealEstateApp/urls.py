from django.urls import path
from . import views
from .views import user_signup,user_login,admin_dashboard,property,dummy

urlpatterns = [
    path('', admin_dashboard.AdminDashboard, name='AdminDashboard'),
    path('signup/', user_signup.signup, name='user_signup'),
    path('login/', user_login.LoginAPIView.as_view(), name='user_login'),
    path('property/', property.PropertyAPIView.as_view(), name='property'),
    path('dummyapi/', dummy.DummyAPIView.as_view(), name='dummyapi'),
    path('updateproperty/<int:pk>',property.UpdateProperty.as_view(), name='updateproperty'),
    path('filterproperty/', property.FilterProperty.as_view(), name='filterproperty'),
    path('PasswordResetRequest/',user_login.PasswordResetRequest.as_view(), name='PasswordResetRequest'),
    path('PasswordReset/',user_login.PasswordReset.as_view(), name='PasswordReset'),

]
