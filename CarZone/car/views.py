from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import QuerySet, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib.parse import urlencode

from .models import Car, CarImage, Manufacturer
from .forms import CarFilterForm, CarCreateForm


def index(request):
    return HttpResponse('PLACEHOLDER VIEW! CHANGE IN URLS.PY!')


def remove(request, pk: int) -> HttpResponseRedirect:
    car: Car = Car.objects.get(pk=pk)

    car.is_available = False
    car.save()

    return redirect('user-posts')


def car_remove_confirm(request, pk: int) -> HttpResponseRedirect:
    car: Car = Car.objects.get(pk=pk)

    context: dict = {
        'pk': pk,
        'brand': car.brand,
        'model': car.model,
    }

    return render(request, template_name='car/remove-confirm.html', context=context)


class CarListView(LoginRequiredMixin, ListView):
    queryset = Car.objects.filter(is_available=True)
    template_name = 'car/catalogue.html'
    ordering = ['pk']
    paginate_by = 3


    def get_context_data(self, *args, **kwargs) -> dict:
        context: dict = super().get_context_data(*args, **kwargs)

        context['form'] = CarFilterForm(
            initial={
                field: self.get_param(field)
                for field in CarFilterForm.base_fields
            }
        )

        page_obj = context['page_obj']
        base_url = self.request.path_info

        if page_obj.has_previous():
            context['first_page_url'], context['prev_page_url'] = self.get_prev_pages_urls(page_obj, base_url)
        if page_obj.has_next():
            context['next_page_url'], context['last_page_url'] = self.get_next_pages_urls(page_obj, base_url)

        return context


    def get_queryset(self) -> QuerySet:
        filtered_queryset: QuerySet = self.filter(super().get_queryset())
        ordering: str = self.request.GET.get('order_by', None)

        return filtered_queryset.order_by(ordering) if ordering else filtered_queryset


    def filter(self, queryset: QuerySet) -> QuerySet:
        lookups: list = [
            'brand__icontains', 'model__icontains',
            'price__gte', 'price__lte',
            'horsepower__gte', 'horsepower__lte',
            'mileage__gte', 'mileage__lte',
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


class ListUserCarView(LoginRequiredMixin, ListView):
    template_name = 'accounts/your-posts.html'
    paginate_by = 6


    def get_queryset(self) -> QuerySet:
        criteria = Q(dealer=self.request.user) & Q(is_available=True)
        return Car.objects.filter(criteria).order_by('pk')


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'car/car-create.html'
    form_class = CarCreateForm
    success_url = reverse_lazy('catalogue')


    def form_valid(self, form) -> None:
        form.instance.dealer = self.request.user
        form.instance.manufacturer = self.get_manufacturer(form.instance.brand.lower())

        form.instance.save()

        self.add_features(form.instance, self.request.POST.getlist('feature'))
        self.add_images(form.instance, self.request.FILES.getlist('images'))

        return super().form_valid(form)


    @staticmethod
    def get_manufacturer(brand: str) -> Manufacturer | None:
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
            'citroen': 'Citroen'
        }

        try:
            return Manufacturer.objects.get(name__iexact=manufacturers[brand])
        except (Manufacturer.DoesNotExist, KeyError):
            return None


    @staticmethod
    def add_features(instance: Car, features: list) -> None:
        instance.features.add(*features)


    @staticmethod
    def add_images(instance: Car, images: list) -> None:
        images_to_create = [CarImage(image=image, car_id=instance.pk) for image in images]
        CarImage.objects.bulk_create(images_to_create)


class CarDetailView(LoginRequiredMixin, DetailView):
    queryset = Car.objects.all()
    template_name = 'car/car-details.html'


    def dispatch(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if not self.get_object().is_available:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs) -> HttpResponse:
        car: Car = self.get_object()

        car.views += 1
        car.save()

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)
        car: Car = self.get_object()

        context['features'] = car.features.order_by('pk')
        context['car_images'] = car.images.order_by('pk')

        return context
