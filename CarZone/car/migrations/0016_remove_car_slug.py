# Generated by Django 5.0.2 on 2024-03-13 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0015_car_slug_alter_car_body_type_alter_car_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='slug',
        ),
    ]