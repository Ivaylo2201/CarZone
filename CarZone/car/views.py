from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, QueryDict
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q
from django.core.paginator import Page
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render

from urllib.parse import urlencode

from .forms import CarFilterForm, CarCreateForm, CarUpdateForm
from .mixins import AvailabilityRequiredMixin, OwnershipRequiredMixin
from .models import Car, CarImage, Manufacturer
from .helpers import get_manufacturer



def remove(_, pk: int) -> HttpResponseRedirect:
    car: Car = Car.objects.get(pk=pk)

    car.is_available = False
    car.save()

    return redirect('user-posts')


def car_remove_confirm(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    car: Car = Car.objects.get(pk=pk)

    context: dict = {
        'pk': pk,
        'brand': car.brand,
        'model': car.model,
    }

    return render(request, template_name='car/remove-confirm.html', context=context)


class CarListView(LoginRequiredMixin, ListView):
    queryset = Car.objects.filter(is_available=True).order_by('pk')
    template_name = 'car/catalogue.html'
    paginate_by = 3

    def get_context_data(self, *args, **kwargs) -> dict:
        context: dict = super().get_context_data(*args, **kwargs)

        context['form'] = CarFilterForm(
            initial={field: self.get_param(field)
                     for field in CarFilterForm.base_fields}
        )

        page_obj: Page = context['page_obj']
        base_url: str = self.request.path_info

        if page_obj.has_previous():
            context['first_page_url'], context['prev_page_url'] = (
                self.get_prev_pages_urls(page_obj, base_url)
            )
        if page_obj.has_next():
            context['next_page_url'], context['last_page_url'] = (
                self.get_next_pages_urls(page_obj, base_url)
            )

        return context

    def get_queryset(self) -> QuerySet:
        return self.order(self.filter(super().get_queryset()))

    def get_ordering(self) -> str | None:
        raw_ordering: str = self.get_param('order_by')

        if raw_ordering is None:
            return None

        map_to_orm: dict = {
            'price_desc': '-price',
            'mileage_desc': '-mileage',
            'horsepower_desc': '-horsepower',
            'manufacture_year_desc': '-manufacture_year',
        }

        return map_to_orm[raw_ordering] if raw_ordering.endswith('_desc') else raw_ordering

    def filter(self, queryset: QuerySet) -> QuerySet:
        lookups: list = [
            'brand__icontains',
            'model__icontains',
            'price__gte',
            'price__lte',
            'horsepower__gte',
            'horsepower__lte',
            'mileage__gte',
            'mileage__lte',
            'capacity__gte',
            'capacity__lte',
        ]

        lookups_and_fields: list[tuple] = zip(
            lookups, CarFilterForm.base_fields)
        filters: dict = {}

        for lookup, field in lookups_and_fields:
            filters[lookup] = self.get_param(field)

        for key, value in filters.items():
            if value:
                queryset = queryset.filter(**{key: value})

        return queryset

    def order(self, queryset: QuerySet) -> QuerySet:
        ordering: str = self.get_ordering()

        return queryset.order_by(ordering) if ordering else queryset

    def get_param(self, field: str) -> str:
        return self.request.GET.get(field, None)

    def get_prev_pages_urls(self, page_obj: Page, base_url: str) -> list:
        page_params: QueryDict = self.request.GET.copy()
        urls: list = []

        page_params['page'] = page_obj.paginator.page_range[0]
        urls.append(f'{base_url}?{urlencode(page_params)}')

        page_params['page'] = page_obj.previous_page_number()
        urls.append(f'{base_url}?{urlencode(page_params)}')

        return urls

    def get_next_pages_urls(self, page_obj: Page, base_url: str) -> list:
        '''
        This is needed because the paginator hrefs replace the query params with page=<page>

        1. Copy the already existing params in a dict -> {'brand': 'Audi'}
        2. Place in the same dict the next/last page -> {'brand': 'Audi', 'page': 2}

        - Urlencode takes a dict and converts it to query params string

        3. Generated url -> localhost:8000/car/catalogue/?brand=Audi&page=2
        '''

        page_params: QueryDict = self.request.GET.copy()
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
        criteria: Q = Q(dealer=self.request.user) & Q(is_available=True)

        return Car.objects.filter(criteria).order_by('pk')


class CarCreateView(LoginRequiredMixin, CreateView):
    template_name = 'car/car-create.html'
    form_class = CarCreateForm
    success_url = reverse_lazy('catalogue')

    def form_valid(self, form) -> HttpResponse:
        form.instance.dealer = self.request.user

        try:
            form.instance.manufacturer = (
                Manufacturer.objects.get(
                    name=get_manufacturer(form.instance.brand.lower()))
            )
        except Manufacturer.DoesNotExist:
            form.instance.manufacturer = None

        form.instance.save()

        self.add_features(form.instance, self.request.POST.getlist('feature'))
        self.add_images(form.instance, self.request.FILES.getlist('images'))

        return super().form_valid(form)

    @staticmethod
    def add_features(instance: Car, features: list) -> None:
        instance.features.add(*features)

    @staticmethod
    def add_images(instance: Car, images: list) -> None:
        images_to_create = [
            CarImage(image=image, car_id=instance.pk) for image in images
        ]
        CarImage.objects.bulk_create(images_to_create)


class CarDetailView(AvailabilityRequiredMixin, LoginRequiredMixin, DetailView):
    queryset = Car.objects.all()
    template_name = 'car/car-details.html'

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


class CarUpdateView(OwnershipRequiredMixin, LoginRequiredMixin, UpdateView):
    queryset = Car.objects.all()
    form_class = CarUpdateForm
    template_name = 'car/car-update.html'

    def get_initial(self) -> dict:
        return self.get_object().__dict__

    def get_success_url(self) -> str:
        return reverse('car-details', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        try:
            self.object.manufacturer = (
                Manufacturer.objects.get(
                    name__iexact=get_manufacturer(self.object.brand.lower()))
            )
        except Manufacturer.DoesNotExist:
            self.object.manufacturer = None

        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)
        car: Car = self.get_object()

        context['brand'] = car.brand
        context['model'] = car.model

        return context
