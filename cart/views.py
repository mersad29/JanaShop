from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from django.contrib import messages

from account.forms import AddressForm
from account.models import Address
from cart.cart_madule import Cart
from cart.forms import Discount_code
from cart.models import Order, OrderItem
from product.models import Product, Discount


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart.html', {'cart': cart})


class CartAddingView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        color, quantity, discount = request.POST.get('color'), request.POST.get(
            'quantity'), product.discount
        cart = Cart(request)
        cart.add(product, quantity, color, discount)
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


# class CheckOutView(View):
#     def get(self, request, pk):
#         form = Discount_code()
#         order = get_object_or_404(Order, id=pk)
#         request.session['order_id'] = order.id
#         return render(request, 'cart/checkout.html', {'form': form, 'order': order})
#
#     def post(self, request, pk):
#         form = Discount_code(request.POST)
#         order = get_object_or_404(Order, id=pk)
#         request.session['order_id'] = order.id
#         if form.is_valid():
#             code = form.cleaned_data.get('code')
#             discount = get_object_or_404(Discount, code=code, is_active=True)
#
#             if discount.is_valid() and order.total_price >= discount.min_order_amount:
#                 order.discount = discount
#                 order.total_price = discount.apply_discount(total_amount=order.total_price)
#                 order.save()
#
#         return redirect('cart:checkout', order.id)

def checkout(request):
    form = Discount_code()
    order = Order.objects.last()

    if request.method == 'POST':
        form = Discount_code(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            discount = Discount.objects.get(code=code)
            order.discount = discount
            order.save()

            messages.success(request, 'کد تخفیف اعمال شد.')

            return redirect('cart:checkout')

    context = {
        'order': order,
        'form': form,
        'total_price': order.total_price,
        'final_price': order.get_final_price(),
        # 'discount_amount': discount.get_discount_amount(),
    }
    return render(request, 'cart/checkout.html', context)



class OrderCreationView(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, phone=request.user.phone, total_price=cart.total_final_price())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], color=item['color']
                                     , price=item['final_price'], quantity=item['quantity'])
        cart.remove_cart()
        return redirect('cart:checkout', str(order.id))


# def apply_discount(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     form = Discount_code(request.POST or None)
#
#     if request.method == "POST" and form.is_valid():
#         code = form.cleaned_data['code']
#         discount = get_object_or_404(Discount, code=code, active=True)
#
#         if discount.is_valid() and order.total_price >= discount.min_order_amount:
#             order.discount = discount
#             order.save()
#             return redirect("order_summary", order_id=order.id)
#
#     return render(request, "cart/checkout.html", {"form": form, "order": order})

class VerifyView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)

        for item in order.items.all():
            item.product.sales += 1
            item.product.save()

        order.is_paid = True
        order.save()

        return render(request, 'cart/verify.html', {'order': order})

class AddressView(View):
    def get(self, request):
        form = AddressForm()
        addresses = request.user.useraddress.all()
        contex = {
            'form': form,
            "addresses": addresses
        }
        return render(request, 'cart/address_list.html', contex)

class AddAddressView(View):
    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user

            if not request.user.useraddress.filter(is_default=True).exists():
                address.is_default = True
            address.save()

        return redirect('cart:address_list')

    def get(self, request):
        form = AddressForm()
        addresses = request.user.useraddress.all()
        contex = {
            'form': form,
            "addresses": addresses
        }
        return render(request, 'cart/add_address.html', contex)

class EditAddressView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'account/edit_address.html'
    success_url = reverse_lazy('cart:address_list')

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

def delete_address(request, id):
    address = get_object_or_404(Address, user=request.user, id=id)
    was_default = address.is_default
    address.delete()

    if was_default:
        remain_address = request.user.useraddress.all()
        if remain_address.exists():
            new_default = remain_address.first()
            new_default.is_default = True
            new_default.save()

    return redirect('cart:address_list')