from django.urls import path, include

from .views import index, CarListView, CarDetailView, CarCreateView

urlpatterns: tuple = (
    path('catalogue/', CarListView.as_view() ,name='catalogue'),
    path('create/', CarCreateView.as_view(), name='car_create'),
    path('<int:pk>/', include(
        [
            path('details/', CarDetailView.as_view(), name='car_details'),
            path('update/', index, name='car_update'),
            path('remove/', index, name='car_remove')
        ]
    ))
)