# Generated by Django 4.1.10 on 2023-08-09 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disposerv', '0015_contractposition_pickup_time_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='gps_lat',
            field=models.FloatField(default=48.216618),
        ),
        migrations.AddField(
            model_name='settings',
            name='gps_lon',
            field=models.FloatField(default=16.385031),
        ),
    ]
