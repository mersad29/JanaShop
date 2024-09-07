from django.urls import path
from . import views

app_name = 'index'
urlpatterns = [
    path('', views.index, name='home'),
    path('faq', views.faq, name='faq'),
    path('about_us', views.about, name='about'),
    path('search', views.search, name='search'),
    path('favorite/add/<int:id>', views.add_to_favorite, name='add_favorite'),
    path('favorite/remove/<int:id>', views.remove_from_favorite, name='delete_favorite'),
]
