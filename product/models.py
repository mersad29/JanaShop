from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from account.models import CustomUser
from product.ProductManager import ProductManager


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,
                               null=True, related_name='subs', verbose_name='دسته بندی های والد')
    title = models.CharField(max_length=35, verbose_name='عنوان دسته بندی')
    image = models.ImageField(upload_to='product/images', blank=True, null=True, verbose_name='تصویر')
    slug = models.SlugField(verbose_name='آدرس')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.title

class FeaturedCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='featured_cat')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.category.title


class Color(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = "رنگ ها"

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = "سایز ها"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'ّبرند'
        verbose_name_plural = "برند ها"

    def __str__(self):
        return self.name


class Product(models.Model):
    in_stock = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    final_price = models.BigIntegerField()
    discount = models.BigIntegerField(blank=True, null=True)
    percent_discount = models.BigIntegerField(blank=True, null=True)
    short_body = models.TextField(max_length=1000, blank=True, null=True)
    color = models.ManyToManyField(Color, related_name='color')
    size = models.ManyToManyField(Size, related_name='size', blank=True, null=True)
    brand = models.ForeignKey(Brand, related_name='brands', blank=True, null=True, on_delete=models.CASCADE)
    review = RichTextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='cat', blank=True, null=True)
    main_image = models.ImageField(upload_to='product/images', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ ثبت')
    view = models.PositiveBigIntegerField(default=0)
    sales = models.PositiveBigIntegerField(default=0)

    dimension = models.CharField(max_length=100, blank=True, null=True, verbose_name='ابعاد')
    weight = models.CharField(max_length=100, blank=True, null=True, verbose_name='وزن')
    SIM = models.CharField(max_length=100, blank=True, null=True, verbose_name='سایز سیمکارت')
    body_material = models.CharField(max_length=100, blank=True, null=True, verbose_name='متریال بدنه')
    SIM_num = models.CharField(max_length=100, blank=True, null=True, verbose_name='تعداد سیمکارت')
    introduction_time = models.CharField(max_length=100, blank=True, null=True, verbose_name='زمان معرفی')

    star = models.PositiveIntegerField(editable=False, default=0)
    empty_star = models.PositiveIntegerField(editable=False, default=5)

    objects = ProductManager()

    def get_current_price(self):

        active_sales = self.special_sales.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).first()

        if active_sales:
            self.final_price = active_sales.sale_price
            return self.final_price
        return self.final_price

    def average_rate(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.value for rating in ratings) / ratings.count()
        return 0

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.slug])

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title)
        super(Product, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = "محصولات"


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product/images')

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = "تصاویر بیشتر"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies',
                               verbose_name='کامنت والد')
    name = models.CharField(max_length=70, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    body = models.TextField(verbose_name='متن')
    is_published = models.BooleanField(default=False, verbose_name='وضعیت انتشار')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return f"{self.name} - {self.email} - {self.product.title}"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')


class SpecialSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='special_sales')
    sale_price = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        return self.start_date <= timezone.now() <= self.end_date
