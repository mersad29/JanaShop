from django.contrib import admin
from .models import Category, Product, ProductImages, Color, Size

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImages

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]