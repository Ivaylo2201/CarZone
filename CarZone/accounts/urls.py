from django.urls import path, include

from .views import logout_then_login, deactivate, initial
from .views import SignUpUserView, SignInUserView, UpdateUserView, DeactivationConfirmTemplateView
from ..car.views import ListUserCarView

urlpatterns: tuple = (
    path('', initial),
    path('accounts/', include(
        [
            path('login/', SignInUserView.as_view(), name='login'),
            path('sign-up/', SignUpUserView.as_view(), name='sign-up'),
            path('logout/', logout_then_login, name='logout'),
            path('profile/', UpdateUserView.as_view(), name='profile'),
            path('posts/', ListUserCarView.as_view(), name='user-posts'),
            path('deactivate/', include(
                [
                    path('confirm/', DeactivationConfirmTemplateView.as_view(), name='deactivate-confirm'),
                    path('', deactivate, name='deactivate-account')
                ]
            )),
        ]
    )),
)
