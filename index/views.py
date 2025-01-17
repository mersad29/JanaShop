from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ad.models import Banners, Carousel, MidBanners
from index.models import Faq, About, Footer
from product.models import Category, Product, SpecialSale, Like, FeaturedCategory
from django.db.models import Count, Q

def index(request):
    carousel = Carousel.objects.all()
    banners = Banners.objects.all().order_by('created_time')
    midbanners = MidBanners.objects.all()
    products = Product.objects.all()
    most_off = products.order_by('-discount')
    most_view = products.order_by('-view')
    most_sale = products.order_by('-sales')
    # socials = Footer.objects.first()

    featured_cats = FeaturedCategory.objects.filter(is_active=True).select_related('category')
    if featured_cats:
        for cat in featured_cats:
            cat.products = cat.category.cat.order_by('-sales')[0:7]

    for query in [most_off, most_view, most_sale]:
        for pr in query:
            pr.final_price = pr.get_current_price()
            if request.user.is_authenticated:
                if Like.objects.filter(user=request.user, product=pr):
                    pr.liked = True
                else:
                    pr.liked = False

    for item in most_off:
        item.comment_count = item.comments.filter(is_published=True).count()

    fire_sales = SpecialSale.objects.all()
    for pr in fire_sales:
        pr.sale_price = pr.product.get_current_price()

        if timezone.now() <= pr.end_date:
            pr.active = True

    context = {
        "carousel": carousel,
        "banners": banners,
        "midbanners": midbanners,
        'most_off': most_off,
        'fire_sales': fire_sales,
        'most_view': most_view,
        'most_sale': most_sale,
        'featured_cats': featured_cats
        # 'socials': socials,
    }
    return render(request, 'index/index.html', context)

def add_to_favorite(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        Like.objects.get_or_create(user=request.user, product=product)
        return redirect('/')
    else:
        return redirect('account:login')

def remove_from_favorite(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        Like.objects.filter(user=request.user, product=product).delete()
        return redirect('/')
    else:
        return redirect('account:login')

def faq(request):
    question = Faq.objects.all()
    return render(request, 'index/faq.html', {'question': question})

def about(request):
    about = About.objects.all().first()
    return render(request, 'index/about.html', {'about': about})

def search(request):
    q = request.GET.get('q')
    product = Product.objects.filter(title__icontains=q).order_by('-created_time')
    recent_product = Product.objects.all().order_by('-created_time')

    min_price = product.order_by('price').first().price
    max_price = product.order_by('price').last().price

    for item in product:
        item.comment = item.comments.filter(is_published=True).count()

    minprice = request.GET.get('minprice')
    maxprice = request.GET.get('maxprice')

    if minprice:
        product = product.filter(price__gte=minprice)

    if maxprice:
        product = product.filter(price__lte=maxprice)

    in_stock_only = request.GET.get('in_stock_only')
    if in_stock_only == 'true':
        product = product.filter(in_stock=True)

    sort = request.GET.get('sort', 'newest')
    if sort == 'min_price':
        product = product.filter().order_by('price')
    if sort == 'max_price':
        product = product.filter().order_by('-price')
    if sort == 'newest':
        product = product.filter().order_by('-created_time')

    context = {
        'product': product,
        'q': q,
        'sort': sort,
        'in_stock_only': in_stock_only,
        'min_price': min_price,
        'max_price': max_price,
        'minprice2': minprice,
        'maxprice2': maxprice,
        'recent_product': recent_product,
    }

    return render(request, 'product/product_list.html', context)