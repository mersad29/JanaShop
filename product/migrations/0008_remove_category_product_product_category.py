# Generated by Django 5.0.3 on 2024-07-08 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_category_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='cat', to='product.category'),
        ),
    ]
