from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import QuerySet
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from typing import Optional
from urllib.parse import urlencode

from .models import Car, CarImage, Manufacturer
from .forms import CarFilterForm, CarCreateForm


def index(request):
    return HttpResponse('PLACEHOLDER VIEW! CHANGE IN URLS.PY!')


class CarListView(LoginRequiredMixin, ListView):
    queryset = Car.objects.all()
    template_name = 'car/catalogue.html'
    ordering = ['pk']
    paginate_by = 3


    def get_context_data(self, *args, **kwargs) -> dict:
        context: dict = super().get_context_data(*args, **kwargs)

        context['form'] = CarFilterForm(
            initial={field: self.get_param(field) for field in CarFilterForm.base_fields}
        )

        page_obj = context['page_obj']
        base_url = self.request.path_info

        if page_obj.has_previous():
            context['first_page_url'], context['prev_page_url'] = self.get_prev_pages_urls(page_obj, base_url)
        if page_obj.has_next():
            context['next_page_url'], context['last_page_url'] = self.get_next_pages_urls(page_obj, base_url)

        return context


    def get_queryset(self) -> QuerySet:
        return self.filter(super().get_queryset())


    def filter(self, queryset: QuerySet) -> QuerySet:
        lookups: list = [
            'brand__icontains', 'model__icontains', 'price__gte', 'price__lte',
            'horsepower__gte', 'horsepower__lte', 'mileage__gte', 'mileage__lte',
            'capacity__gte', 'capacity__lte'
        ]

        lookups_and_fields: list[tuple] = zip(lookups, CarFilterForm.base_fields)
        filters: dict = {}

        for lookup, field in lookups_and_fields:
            filters[lookup] = self.get_param(field)

        for key, value in filters.items():
            if value:
                queryset = queryset.filter(**{key: value})

        return queryset


    def get_param(self, field: str) -> str:
        return self.request.GET.get(field, None)


    def get_prev_pages_urls(self, page_obj: object, base_url: str) -> list[str]:
        page_params = self.request.GET.copy()
        urls: list = []

        page_params['page'] = page_obj.paginator.page_range[0]
        urls.append(f'{base_url}?{urlencode(page_params)}')

        page_params['page'] = page_obj.previous_page_number()
        urls.append(f'{base_url}?{urlencode(page_params)}')

        return urls


    def get_next_pages_urls(self, page_obj: object, base_url: str) -> list[str]:
        page_params = self.request.GET.copy()
        urls: list = []

        page_params['page'] = page_obj.next_page_number()
        urls.append(f'{base_url}?{urlencode(page_params)}')

        page_params['page'] = page_obj.paginator.num_pages
        urls.append(f'{base_url}?{urlencode(page_params)}')

        return urls


class CarCreateView(LoginRequiredMixin, CreateView):
    queryset = Car.objects.all()
    template_name = 'car/car-create.html'
    form_class = CarCreateForm
    success_url = reverse_lazy('catalogue')


    def form_valid(self, form) -> None:
        form.instance.dealer = self.request.user
        form.instance.manufacturer = self.get_manufacturer(form.instance.brand.lower())

        form.instance.save()

        for feature in self.request.POST.getlist('feature'):
            form.instance.features.add(int(feature))

        for image in self.request.FILES.getlist('images'):
            image = CarImage(image=image, car_id=form.instance.pk)
            image.save()
            form.instance.images.add(image)

        return super().form_valid(form)


    @staticmethod
    def get_manufacturer(brand: str) -> Optional[Manufacturer]:
        manufacturers: dict = {
            'audi': 'Volkswagen',
            'vw': 'Volkswagen',
            'seat': 'Volkswagen',
        }

        try:
            return Manufacturer.objects.get(name=manufacturers[brand])
        except (Manufacturer.DoesNotExist, KeyError):
            return None


class CarDetailView(LoginRequiredMixin, DetailView):
    queryset = Car.objects.all()
    template_name = 'car/car-details.html'


    def get(self, request, *args, **kwargs):
        car: Car = self.get_object()
        car.views += 1
        car.save()

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)

        context['features'] = (
            self.get_object()
            .features
            .order_by('pk')
        )

        return context
