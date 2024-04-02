# Generated by Django 5.0.3 on 2024-04-02 10:11

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'رنگ',
                'verbose_name_plural': 'رنگ ها',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'سایز',
                'verbose_name_plural': 'سایز ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('short_body', models.CharField(blank=True, max_length=1000, null=True)),
                ('review', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('color', models.ManyToManyField(related_name='color', to='product.color')),
                ('size', models.ManyToManyField(blank=True, null=True, related_name='size', to='product.size')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='نام')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('body', models.TextField(verbose_name='متن')),
                ('is_published', models.BooleanField(default=False, verbose_name='وضعیت انتشار')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='product.comment', verbose_name='کامنت والد')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='product.product', verbose_name='محصول')),
            ],
        ),
    ]
