# Generated by Django 5.0.2 on 2024-03-17 09:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0017_remove_manufacturer_nationality_manufacturer_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='posted_on',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
