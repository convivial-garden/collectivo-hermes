# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-09-28 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disposerv', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='timesrecord',
            index=models.Index(fields=['date', 'start_datetime', 'end_datetime', 'mode', 'staff_member'], name='disposerv_t_date_978892_idx'),
        ),
    ]