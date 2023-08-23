# Generated by Django 4.1.10 on 2023-08-23 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disposerv', '0021_rename_costumer_contractposition_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='opening_hours',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_blacklisted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_blacklisted_memo',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='customer',
            name='memo',
            field=models.TextField(blank=True),
        ),
    ]
