from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from cart.cart_madule import Cart
from cart.models import Order, OrderItem
from product.models import Product


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart.html', {'cart': cart})

class CartAddingView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        color, size, quantity, discount = request.POST.get('color'), request.POST.get('size'), request.POST.get('quantity')\
            , product.discount
        cart = Cart(request)
        cart.add(product, quantity, color, size, discount)
        return redirect('cart:cart_detail')

def cart_removing(request):
    cart = Cart(request)
    cart.remove_cart()
    return redirect('cart:cart_detail')

class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')

class CheckOutView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        request.session['order_id'] = order.id
        order.address = order.user.useraddress.get(is_default=True)
        order.save()

        return render(request, 'cart/checkout.html', {'order': order})

class OrderCreationView(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, phone=request.user.phone, total_price=cart.total_final_price())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], color=item['color'],
                                     size=item['size'], price=item['final_price'], quantity=item['quantity'])
        # cart.remove_cart()
        print(order.id)
        return redirect('cart:checkout', str(order.id))

class VerifyView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        order.is_paid = True
        order.save()

        return render(request, 'cart/verify.html', {'order': order})