import datetime
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from persiantools.jdatetime import JalaliDate
from . import models
from .models import Comment, Like, Product, Category, Rating


def product_detail(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    product.get_current_price()
    comments = product.comments.all()
    comments_count = comments.filter(product=product, is_published=True).count()
    average_rating = product.average_rate()
    empty_stars = range(int(round(5-average_rating)))

    product.view += 1

    if request.user.is_authenticated:
        if Like.objects.filter(user=request.user, product=product):
            product.liked = True
        else:
            product.liked = False

    product.discount = int(product.price) - int(product.final_price)
    product.percent_discount = (product.discount * 100) // product.price

    for comment in comments:
        created_at = comment.created_time
        comment.jalali = JalaliDate(datetime.date(year=created_at.year, month=created_at.month,
                                                  day=created_at.day)).strftime('%c', 'fa')
        comment.created_time = comment.jalali

    if request.method == 'POST':
        name = request.user.id
        phone = request.user.phone
        email = request.user.email
        body = request.POST.get('body')
        parent = request.POST.get('parent')
        Comment.objects.create(product=product, name=name, email=email or phone, body=body, parent_id=parent)
        rating_value = int(request.POST.get('rating', 0))
        if 1 <= rating_value <= 5:
            Rating.objects.update_or_create(
                product=product, user=request.user,
                value=rating_value
            )
        messages.success(request, "از دیگاه شما متشکریم!")

        product.star = int(round(average_rating))
        product.empty_star = int(round(5-average_rating))
    product.save()

    contex = {
        'product': product,
        'comments_count': comments_count,
        'stars': range(int(round(average_rating))),
        'empty_stars': empty_stars
    }
    return render(request, 'product/product_detail.html', contex)

def add_to_favorite(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        Like.objects.get_or_create(user=request.user, product=product)
        return redirect('product:product_detail', product.slug)
    else:
        return redirect('account:login')


def remove_from_favorite(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        Like.objects.filter(user=request.user, product=product).delete()
        return redirect('product:product_detail', product.slug)
    else:
        return redirect('account:login')

def favorites(request):
    favorites = Like.objects.filter(user=request.user)
    for item in favorites:
         item.comments = item.product.comments.filter(is_published=True).count()
    return render(request, 'account/favorite.html', {'favorite': favorites})

def product_list(request, slug):
    category = Category.objects.get(slug=slug)
    recent_product = Product.objects.all().order_by('-created_time')
    products = Product.objects.filter(category=category).order_by('-created_time')

    min_price = Product.objects.filter(category=category).order_by('price').first().price
    max_price = Product.objects.filter(category=category).order_by('price').last().price


    minprice = request.GET.get('minprice')
    maxprice = request.GET.get('maxprice')

    if minprice:
        products = products.filter(category=category, price__gte=minprice)

    if maxprice:
        products = products.filter(category=category, price__lte=maxprice)

    in_stock_only = request.GET.get('in_stock_only')
    if in_stock_only == 'true':
        products = products.filter(category=category, in_stock=True)

    sort = request.GET.get('sort', 'newest')
    if sort == 'min_price':
        products = products.filter(category=category).order_by('price')
    if sort == 'max_price':
        products = products.filter(category=category).order_by('-price')
    if sort == 'newest':
        products = products.filter(category=category).order_by('-created_time')

    for pr in products:
        pr.comment_count = pr.comments.filter(is_published=True).count()

    # pageinator = Paginator(products, 2)
    # page_num = request.GET.get('page')
    # products = pageinator.get_page(page_num)


    if products:
        context = {
            'products': products,
            'category2': category,
            'sort': sort,
            'in_stock_only': in_stock_only,
            'min_price': min_price,
            'max_price': max_price,
            'minprice2': minprice,
            'maxprice2': maxprice,
            'recent_product': recent_product,
        }
        return render(request, 'product/product_list.html', context)
    else:
        context = {
            'recent_product': recent_product,
        }
        return render(request, 'product/product_list.html', context)

