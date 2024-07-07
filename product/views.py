import datetime
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from persiantools.jdatetime import JalaliDate
from . import models
from .models import Comment


def product_detail(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    comments = product.comments.all()
    if product.discount:
        product.final_price = int(product.price - (product.price * (product.discount / 100)))

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
    }
    return render(request, 'product/product_detail.html', contex)