from django.shortcuts import render
from ad.models import Banners, Carousel, MidBanners
from index.models import Faq
from product.models import Category

def index(request):
    carousel = Carousel.objects.all()
    banners = Banners.objects.all().order_by('created_time')
    midbanners = MidBanners.objects.all()

    context = {
        "carousel": carousel,
        "banners": banners,
        "midbanners": midbanners,
    }
    return render(request, 'index/index.html', context)

def faq(request):
    question = Faq.objects.all()
    # print(question.)
    return render(request, 'index/faq.html', {'question': question})
