# Generated by Django 5.0.3 on 2024-07-28 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ثبت'),
        ),
    ]
