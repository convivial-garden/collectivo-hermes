# Generated by Django 4.1.10 on 2023-08-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disposerv', '0018_repeatedcontractposition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='repeated_deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
