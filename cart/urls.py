from django.urls import path

from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail',),
    path('add/<int:pk>', views.CartAddingView.as_view(), name='cart_add'),
    path('del/<str:id>', views.CartDeleteView.as_view(), name='cart_delete'),
    path('remove', views.cart_removing, name='cart_remove'),
    path('order/<int:pk>', views.CheckOutView.as_view(), name='checkout'),
    path('order/add', views.OrderCreationView.as_view(), name='add_order'),
    path('order/verify/<int:pk>', views.VerifyView.as_view(), name='verify')
]