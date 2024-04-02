from django.shortcuts import render, get_object_or_404
from . import models

def product_detail(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    image = product.product_images.all()
    contex = {
        'product': product,
        'image':image
    }
    return render(request, 'product/product_detail.html', contex)