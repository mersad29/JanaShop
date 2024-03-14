from django.db import models
# from ckeditor.fields import RichTextField


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


# class Color(models.Model):
#     name = models.CharField(max_length=50)
#
#     class Meta:
#         verbose_name = 'رنگ'
#         verbose_name_plural = "رنگ ها"
#
#     def __str__(self):
#         return self.name
#
#
# class Size(models.Model):
#     name = models.CharField(max_length=20)
#
#     class Meta:
#         verbose_name = 'سایز'
#         verbose_name_plural = "سایز ها"
#
#     def __str__(self):
#         return self.name
#
#
# class Product(models.Model):
#     title = models.CharField(max_length=100)
#     price = models.IntegerField()
#     short_body = models.CharField(max_length=1000, blank=True, null=True)
#     color = models.ManyToManyField(Color, related_name='color')
#     size = models.ManyToManyField(Size, related_name='size', blank=True, null=True)
#     review = RichTextField(blank=True, null=True)
