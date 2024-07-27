import datetime
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from persiantools.jdatetime import JalaliDate
from . import models
from .models import Comment, Like, Product


def product_detail(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    comments = product.comments.all()
    comments_count = comments.filter(product=product, is_published=True).count()

    if Like.objects.filter(user=request.user, product=product):
        product.liked = True

    else:
        product.liked = False


    if product.discount:
        product.final_price = int(product.price - (int(product.price) * int(product.percent_discount / 100)))
        product.discount = int(product.price) - int(product.final_price)
    product.save()

    for comment in comments:
        created_at = comment.created_time
        comment.jalali = JalaliDate(datetime.date(year=created_at.year, month=created_at.month,
                                                  day=created_at.day)).strftime('%c', 'fa')
        comment.created_time = comment.jalali

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        body = request.POST.get('body')
        parent = request.POST.get('parent')
        Comment.objects.create(product=product, name=name, email=email, body=body, parent_id=parent)
        messages.success(request, "thanks")

    contex = {
        'product': product,
        'comments_count': comments_count,
    }
    return render(request, 'product/product_detail.html', contex)

def add_to_favorite(request, id):
    product = get_object_or_404(Product, id=id)
    Like.objects.get_or_create(user=request.user, product=product)
    return redirect('product:product_detail', product.slug)

def remove_from_favorite(request, id):
    product = get_object_or_404(Product, id=id)
    Like.objects.filter(user=request.user, product=product).delete()
    return redirect('product:product_detail', product.slug)

def favorites(request):
    favorites = Like.objects.filter(user=request.user)
    for item in favorites:
         item.comments = item.product.comments.filter(is_published=True).count()
    return render(request, 'account/favorite.html', {'favorite': favorites})