from django.contrib import admin
from cart import models


class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_paid')
    inlines = (OrderItemAdmin,)