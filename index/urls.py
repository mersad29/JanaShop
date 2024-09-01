from django.urls import path
from . import views

app_name = 'index'
urlpatterns = [
    path('', views.index, name='home'),
    path('faq', views.faq, name='faq'),
    path('about_us', views.about, name='about'),
]