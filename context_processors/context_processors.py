from django.shortcuts import get_object_or_404

from cart.cart_madule import Cart
from cart.models import Order
from index.models import Footer
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


def socials(request):
    socials = Footer.objects.first()
    return {'socials': socials}

def footer(request):
    footer_detail = Footer.objects.first()
    return {'footer': footer_detail}
