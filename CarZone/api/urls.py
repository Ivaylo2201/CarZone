from django.urls import path, include

from .views import CarListAPIView, CarUpdateAPIView, CarDestroyAPIView, CarRetrieveAPIView
from .views import ManufacturerListCreateAPIView, ManufacturerRetrieveAPIView, ManufacturerUpdateAPIView
from .views import FeatureListCreateAPIView, FeatureRetrieveAPIView, FeatureUpdateAPIView

urlpatterns: tuple = (
    path('car/', include(
        [
            path('list/', CarListAPIView.as_view()),
            path('<int:pk>/', include(
                [
                    path('', CarRetrieveAPIView.as_view()),
                    path('update/', CarUpdateAPIView.as_view()),
                    path('destroy/', CarDestroyAPIView.as_view())
                ]
            ))
        ]
    )),
    path('manufacturer/', include(
        [
            path('list/', ManufacturerListCreateAPIView.as_view()),
            path('<int:pk>/', include(
                [
                    path('', ManufacturerRetrieveAPIView.as_view()),
                    path('update/', ManufacturerUpdateAPIView.as_view()),
                ]
            ))
        ]
    )),
    path('feature/', include(
        [
            path('list/', FeatureListCreateAPIView.as_view()),
            path('<int:pk>/', include(
                [
                    path('', FeatureRetrieveAPIView.as_view()),
                    path('update/', FeatureUpdateAPIView.as_view()),
                ]
            ))
        ]
    ))
)
