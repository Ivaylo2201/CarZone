from django.urls import path, include

from .views import index, CarListView, CarDetailView, CarCreateView, remove, car_remove_confirm

urlpatterns: tuple = (
    path('catalogue/', CarListView.as_view(), name='catalogue'),
    path('create/', CarCreateView.as_view(), name='car-create'),
    path('<int:pk>/', include(
        [
            path('details/', CarDetailView.as_view(), name='car-details'),
            path('update/', index, name='car-update'),
            path('remove/', include(
                [
                    path('confirm/', car_remove_confirm, name='car-remove-confirm'),
                    path('', remove, name='car-remove')
                ]
            ))
        ]
    ))
)
