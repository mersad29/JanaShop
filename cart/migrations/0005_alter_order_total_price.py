# Generated by Django 5.0.3 on 2024-09-07 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.BigIntegerField(default=0, max_length=25),
        ),
    ]
