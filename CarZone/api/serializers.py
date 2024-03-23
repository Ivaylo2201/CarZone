from rest_framework import serializers

from ..car.models import Car, Manufacturer, Feature
from ..accounts.models import CarZoneUser

# MANUFACTURER SERIALIZERS


class ManufacturerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ManufacturerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        exclude = ('id',)


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

# CAR SERIALIZERS


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarZoneUser
        fields = (
            'id', 'first_name', 'last_name',
            'phone_number', 'location', 'profile_picture'
        )


class CarListSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(many=False)
    dealer = DealerSerializer(many=False)

    class Meta:
        model = Car
        fields = '__all__'


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        exclude = ('is_available', 'posted_on',
                   'manufacturer', 'dealer', 'views')


class CarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        exclude = ('id', 'is_available', 'posted_on',
                   'manufacturer', 'dealer', 'views', 'features')

# FEATURE SERIALIZERS

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
