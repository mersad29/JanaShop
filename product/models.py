from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from account.models import CustomUser


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
    is_stock = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    final_price = models.IntegerField()
    discount = models.IntegerField()
    percent_discount = models.IntegerField(blank=True, null=True)
    short_body = models.TextField(max_length=1000, blank=True, null=True)
    color = models.ManyToManyField(Color, related_name='color')
    size = models.ManyToManyField(Size, related_name='size', blank=True, null=True)
    brand = models.ForeignKey(Brand, related_name='brands', blank=True, null=True, on_delete=models.CASCADE)
    review = RichTextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='cat', blank=True, null=True)
    main_image = models.ImageField(upload_to='product/images', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ ثبت')

    dimension = models.CharField(max_length=100, blank=True, null=True, verbose_name='ابعاد')
    weight = models.CharField(max_length=100, blank=True, null=True, verbose_name='وزن')
    SIM = models.CharField(max_length=100, blank=True, null=True, verbose_name='سایز سیمکارت')
    body_material = models.CharField(max_length=100, blank=True, null=True, verbose_name='متریال بدنه')
    SIM_num = models.CharField(max_length=100, blank=True, null=True, verbose_name='تعداد سیمکارت')
    introduction_time = models.CharField(max_length=100, blank=True, null=True, verbose_name='زمان معرفی')

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.slug])

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(Product, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='محصول'
        verbose_name_plural="محصولات"

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product/images')

    class Meta:
        verbose_name='تصویر'
        verbose_name_plural="تصاویر بیشتر"

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



