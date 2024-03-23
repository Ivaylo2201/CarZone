from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import CarListSerializer, CarUpdateSerializer
from .serializers import ManufacturerListSerializer, ManufacturerUpdateSerializer
from .serializers import FeatureSerializer

from ..car.models import Car, Manufacturer, Feature

# CAR API VIEWS


class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    permission_classes = [IsAuthenticated]


class CarRetrieveAPIView(RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    permission_classes = [IsAuthenticated]


class CarUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarUpdateSerializer
    permission_classes = [IsAuthenticated]


class CarDestroyAPIView(DestroyAPIView):
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        car: Car = self.get_object()
        car.is_available = False
        car.save()

        return Response('Car marked as unavailable', status=HTTP_200_OK)

# MANUFACTURER API VIEWS


class ManufacturerListCreateAPIView(ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerListSerializer
    permission_classes = [IsAuthenticated]


class ManufacturerRetrieveAPIView(RetrieveAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerListSerializer
    permission_classes = [IsAuthenticated]


class ManufacturerUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerUpdateSerializer
    permission_classes = [IsAuthenticated]

# FEATURE API VIEWS


class FeatureListCreateAPIView(ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticated]


class FeatureRetrieveAPIView(RetrieveAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticated]


class FeatureUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticated]
