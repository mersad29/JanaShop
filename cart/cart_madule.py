from product.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(item['price'])
            item['total_discount'] = int(item['quantity']) * int(item['discount'])
            item['final_price'] = item['total'] - item['total_discount']
            item['unique_id'] = self.unique_id_generator(product.id, item['color'])
            yield item

    def unique_id_generator(self, id, color):
        result = f"{id}-{color}"

        return result

    def add(self, product, quantity, color, discount):
        unique = self.unique_id_generator(product.id, color)

        if unique not in self.cart:
            self.cart[unique] = {'quantity': 0, 'price': product.price, 'color': color, 'id': product.id,
                                 'discount': discount}

        self.cart[unique]['quantity'] += int(quantity)
        self.save()

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def total(self):
        cart = self.cart.values()
        total_price = 0
        for item in cart:
            total_price += int(item['quantity']) * int(item['price'])
        return total_price

    def total_discount(self):
        cart = self.cart.values()
        total_discount = 0
        for item in cart:
            total_discount += int(item['quantity']) * int(item['discount'])
        return total_discount

    def total_final_price(self):
        cart = self.cart.values()
        total_final_price = 0
        for item in cart:
            total_final_price += int(int(item['quantity']) * int(item['price'])) - int(
                int(item['quantity']) * int(item['discount']))
        return total_final_price

    def save(self):
        self.session.modified = True

    def remove_cart(self):
        del self.session[CART_SESSION_ID]

    def count(self):
        cart = self.cart.values()
        count = 0
        for item in cart:
            count += item['quantity']
        return count
