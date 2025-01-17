from django.contrib import admin
from django import forms
from .models import Category, Product, ProductImages, Color, Size, Comment, Like, SpecialSale, Rating

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImages

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

class LikeAdmin(admin.TabularInline):
    model = Like

admin.site.register(Like)
admin.site.register(SpecialSale)
admin.site.register(Rating)
