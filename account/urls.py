from django.urls import path
from .views import RegisterOrLogin, CheckOtp, user_logout, profile

app_name = 'account'
urlpatterns = [
    path('login', RegisterOrLogin.as_view(), name='login'),
    path('checkotp', CheckOtp.as_view(), name='check_otp'),
    path('logout', user_logout, name='logout'),
    path('profile', profile, name='profile')
]