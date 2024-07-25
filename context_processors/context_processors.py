from cart.cart_madule import Cart
from product.models import Category


def category(request):
    categories = Category.objects.all()

    return {'categories': categories}

def cart_count(request):
    cart = Cart(request).count()

    return {'cart_count': cart}
