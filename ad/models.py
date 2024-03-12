from django.db import models

class Carousel(models.Model):
    name = models.CharField(max_length=50, verbose_name='عنوان تصویر')
    image = models.ImageField(upload_to='ad/images', verbose_name='تصویر')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    class Meta:
        verbose_name = 'تصویر اسلایدی هدر'
        verbose_name_plural = 'تصاویر اسلایدی هدر'

    def __str__(self):
        return f"{self.name} - {self.created_time}"

class Banners(models.Model):
    name = models.CharField(max_length=50, verbose_name='عنوان تصویر')
    image = models.ImageField(upload_to='ad/images', verbose_name='تصویر')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    class Meta:
        verbose_name = 'تصویر بنر'
        verbose_name_plural = 'تصاویر بنر ها'

    def __str__(self):
        return f"{self.name} - {self.created_time}"

class MidBanners(models.Model):
    name = models.CharField(max_length=50, verbose_name='عنوان تصویر')
    image = models.ImageField(upload_to='ad/images', verbose_name='تصویر')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    class Meta:
        verbose_name = 'تصویر بنر میانه سایت'
        verbose_name_plural = 'تصاویر بنر های میانه سایت'

    def __str__(self):
        return f"{self.name} - {self.created_time}"