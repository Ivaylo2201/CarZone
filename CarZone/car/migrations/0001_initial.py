# Generated by Django 5.0.2 on 2024-03-09 10:45

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='manufacturers/')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=25)),
                ('model', models.CharField(max_length=25)),
                ('manufacture_year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2024)])),
                ('transmission_type', models.CharField(choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')], max_length=15)),
                ('horsepower', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(750)])),
                ('capacity', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5000)])),
                ('euro_standard', models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], null=True)),
                ('mileage', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(750000)])),
                ('body_type', models.CharField(choices=[('Sedan', 'Sedan'), ('Coupe', 'Coupe'), ('Wagon', 'Wagon'), ('Hatchback', 'Hatchback')], max_length=20)),
                ('fuel_type', models.CharField(choices=[('Bensine', 'Bensine'), ('Diesel', 'Diesel'), ('Gas', 'Gas'), ('Electric', 'Electric')], max_length=15)),
                ('color', models.CharField(choices=[('White', 'White'), ('Grey', 'Grey'), ('Black', 'Black'), ('Red', 'Red'), ('Blue', 'Blue'), ('Yellow', 'Yellow'), ('Orange', 'Orange'), ('Green', 'Green')], max_length=15)),
                ('price', models.PositiveIntegerField()),
                ('warranty', models.PositiveSmallIntegerField(default=0)),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('features', models.ManyToManyField(to='car.feature')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars', to='car.manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cars/')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='car.car')),
            ],
        ),
    ]
