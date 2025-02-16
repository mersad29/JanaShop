import uuid

from django.db import models
from account.models import CustomUser, Address
from product.models import Product, Discount


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.IntegerField(max_length=12)
    total_price = models.BigIntegerField(default=0)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    paid_time = models.DateTimeField(blank=True, null=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)

    def get_final_price(self):
        if self.discount and self.discount.is_valid():
            return self.discount.apply_discount(self.total_price)
        return self.total_price



    def __str__(self):
        return f"{self.phone} - {self.id} - {self.created_time}"

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items_p')
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    quantity = models.SmallIntegerField()
    price = models.PositiveBigIntegerField()

    def get_one_price(self):
        price_per_one = self.price / self.quantity
        return price_per_one