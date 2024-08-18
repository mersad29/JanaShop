from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('favorite/add/<int:id>', views.add_to_favorite, name='add_favorite'),
    path('favorite/remove/<int:id>', views.remove_from_favorite, name='delete_favorite'),
    path('list/cat=<slug:slug>', views.product_list, name='product_list'),
]