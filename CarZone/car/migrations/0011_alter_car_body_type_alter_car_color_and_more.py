# Generated by Django 5.0.2 on 2024-03-12 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0010_alter_car_color_alter_car_euro_standard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='body_type',
            field=models.CharField(choices=[('', 'Select body type'), ('Sedan', 'Sedan'), ('Coupe', 'Coupe'), ('Wagon', 'Wagon'), ('Hatchback', 'Hatchback'), ('SUV', 'SUV'), ('Limousine', 'Limousine'), ('Pickup', 'Pickup'), ('Van', 'Van')], default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='car',
            name='color',
            field=models.CharField(choices=[('', 'Select a color'), ('White', 'White'), ('Grey', 'Grey'), ('Black', 'Black'), ('Red', 'Red'), ('Blue', 'Blue'), ('Yellow', 'Yellow'), ('Orange', 'Orange'), ('Green', 'Green')], max_length=15),
        ),
        migrations.AlterField(
            model_name='car',
            name='fuel_type',
            field=models.CharField(choices=[('', 'Select fuel type'), ('Bensine', 'Bensine'), ('Diesel', 'Diesel'), ('Gas', 'Gas'), ('Electric', 'Electric')], default=None, max_length=15),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission_type',
            field=models.CharField(choices=[('', 'Select transmission type'), ('Automatic', 'Automatic'), ('Manual', 'Manual')], default=None, max_length=15),
        ),
    ]
