from django.shortcuts import render
from django.utils import timezone

from ad.models import Banners, Carousel, MidBanners
from index.models import Faq, About
from product.models import Category, Product, SpecialSale
from django.db.models import Count, Q


def index(request):
    carousel = Carousel.objects.all()
    banners = Banners.objects.all().order_by('created_time')
    midbanners = MidBanners.objects.all()
    products = Product.objects.all()
    most_off = Product.objects.all().order_by('-discount')
    most_view = products.order_by('-view')
    most_sale = products.order_by('-sales')

    for item in most_off:
        item.comment_count = item.comments.filter(is_published=True).count()

    fire_sale = SpecialSale.objects.all().first()
    fire_sale.sale_price = fire_sale.product.get_current_price()

    if timezone.now() <= fire_sale.end_date:

        fire_sale.active = True

    context = {
        "carousel": carousel,
        "banners": banners,
        "midbanners": midbanners,
        'most_off': most_off,
        'fire_sale': fire_sale,
        'most_view': most_view,
        'most_sale': most_sale,
    }
    return render(request, 'index/index.html', context)

def faq(request):
    question = Faq.objects.all()
    return render(request, 'index/faq.html', {'question': question})

def about(request):
    about = About.objects.all().first()
    return render(request, 'index/about.html', {'about': about})