from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse

from .models import Manufacturer


class AvailabilityRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if not self.get_object().is_available:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnershipRequiredMixin(AccessMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if self.request.user.pk != self.get_object().dealer.pk:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ManufacturerMixin:
    def get_manufacturer(request, brand: str) -> Manufacturer | None:
        manufacturers: dict = {
            'audi': 'Volkswagen',
            'vw': 'Volkswagen',
            'seat': 'Volkswagen',
            'lamborghini': 'Volkswagen',
            'porsche': 'Volkswagen',
            'toyota': 'Toyota',
            'fiat': 'Fiat',
            'bmw': 'BMW',
            'mercedes-benz': 'Mercedes-Benz',
            'nissan': 'Nissan',
            'hyundai': 'Hyundai',
            'kia': 'Hyundai',
            'volvo': 'Volvo',
            'mazda': 'Mazda',
            'renault': 'Renault',
            'peugeot': 'Peugeot',
            'citroen': 'Citroen',
            'maserati': 'Maserati',
            'ferrari': 'Ferrari'
        }

        try:
            return Manufacturer.objects.get(name__iexact=manufacturers[brand])
        except (Manufacturer.DoesNotExist, KeyError):
            return None