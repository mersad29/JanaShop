import uuid

from django.db import models
from account.models import CustomUser
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.IntegerField(max_length=12)
    total_price = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.phone

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items_p')
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    quantity = models.SmallIntegerField()
    price = models.PositiveIntegerField()