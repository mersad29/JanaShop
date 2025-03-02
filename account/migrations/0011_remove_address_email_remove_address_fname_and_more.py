# Generated by Django 5.0.3 on 2024-07-20 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='email',
        ),
        migrations.RemoveField(
            model_name='address',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='address',
            name='lname',
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='telephone',
            field=models.IntegerField(default=1, max_length=12),
            preserve_default=False,
        ),
    ]
