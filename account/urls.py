from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login', views.RegisterOrLogin.as_view(), name='login'),
    path('checkotp', views.CheckOtp.as_view(), name='check_otp'),
    path('logout', views.user_logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('address_list', views.AddressView.as_view(), name='address_list'),
    path('add/address', views.AddAddressView.as_view(), name='add_address'),
    path('edit_address/<int:pk>', views.EditAddressView.as_view(), name='edit_address'),
    path('set_default/<int:id>', views.Set_default_address.as_view(), name='set_default'),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
]