import datetime
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from persiantools.jdatetime import JalaliDate
from . import models
from .forms import ProductFilterForm
from .models import Comment, Like, Product, Category


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

def product_list(request, slug):
    category = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=category)
    max_price = int(product.order_by('-price').first().price)

    for item in product:
        item.comment = item.comments.filter(is_published=True).count()

    form = ProductFilterForm(request.GET or None)

    if form.is_valid():
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        in_stock = form.cleaned_data.get('in_stock')
        sort_by = form.cleaned_data.get('sort_by')

        if category:
            product = product.filter(category__icontains=category)
        if min_price is not None:
            product = product.filter(price__gte=min_price)
        if max_price is not None:
            product = product.filter(price__lte=max_price)
        if in_stock is not None:
            product = product.filter(in_stock=in_stock)
        if sort_by:
            if sort_by == 'newest':
                product = product.order_by('-created_at')
            elif sort_by == 'greatest':
                product = product.order_by('-rating')
            elif sort_by == 'most_popular':
                product = product.order_by('-sales_count')

    context = {
        'product': product,
        'max_price': max_price,
        'form': form
    }

    return render(request, 'product/product_list.html', context)