# Generated by Django 5.0.3 on 2024-04-01 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='national_code',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
