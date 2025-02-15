from django.urls import path

from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail', ),
    path('add/<int:pk>', views.CartAddingView.as_view(), name='cart_add'),
    path('del/<str:id>', views.CartDeleteView.as_view(), name='cart_delete'),
    path('remove', views.cart_removing, name='cart_remove'),
    # path('order/<int:pk>', views.CheckOutView.as_view(), name='checkout'),
    path('order/<int:pk>', views.checkout, name='checkout'),
    path('order/add', views.OrderCreationView.as_view(), name='add_order'),
    path('order/request', views.send_request, name='request'),
    # path('order/verify/<int:pk>', views.VerifyView.as_view(), name='verify'),
    path('order/verify/<int:pk>', views.verify, name='verify'),
    path('order/factor/<int:pk>', views.FactorDetail.as_view(), name='factor'),
    path('address_list', views.AddressView.as_view(), name='address_list'),
    path('add/address', views.AddAddressView.as_view(), name='add_address'),
    path('edit_address/<int:pk>', views.EditAddressView.as_view(), name='edit_address'),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
]
