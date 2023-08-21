# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-09-28 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disposerv', '0002_auto_20190928_1016'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='contractposition',
            index=models.Index(fields=['start_time'], name='disposerv_c_start_t_2ae8bf_idx'),
        ),
        migrations.AddIndex(
            model_name='street',
            index=models.Index(fields=['name', 'name_street', 'nr_von', 'nr_bis'], name='disposerv_s_name_0ad964_idx'),
        ),
    ]