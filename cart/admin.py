from django.contrib import admin
from cart import models
from product.models import Discount


class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_paid')
    inlines = (OrderItemAdmin,)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code',)
    search_fields = ('code',)
