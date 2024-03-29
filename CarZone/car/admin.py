from django.contrib import admin
from .models import Car, Manufacturer


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'brand', 'model', 'manufacture_year', 'transmission_type',
        'horsepower', 'capacity', 'euro_standard', 'mileage',
        'body_type', 'fuel_type', 'color', 'price', 'dealer',
        'warranty', 'is_available', 'posted_on'
    ]

    ordering = ['-posted_on']
    list_filter = ['manufacture_year', 'horsepower', 'capacity', 'euro_standard', 'mileage', 'price']
    search_fields = ['brand', 'model', 'transmission_type', 'body_type', 'fuel_type', 'color']
    readonly_fields = ['dealer', 'is_available']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'country']
    list_filter = ['country']
    ordering = ['name']
    search_fields = ['name', 'country']
    list_per_page = 15
