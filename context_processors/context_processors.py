from django.shortcuts import get_object_or_404

from cart.cart_madule import Cart
from cart.models import Order
from product.models import Category, Product


def category(request):
    categories = Category.objects.all()

    return {'categories': categories}


def cart_count(request):
    cart = Cart(request).count()

    return {'cart_count': cart}


def last_orders(request):
    # order = Order.objects.filter(is_paid=True)
    # return {'order': order}
    pass
