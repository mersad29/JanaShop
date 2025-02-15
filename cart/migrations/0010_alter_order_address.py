# Generated by Django 5.0.3 on 2025-02-15 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_rename_expiration_date_otp_created_at'),
        ('cart', '0009_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.address'),
        ),
    ]
