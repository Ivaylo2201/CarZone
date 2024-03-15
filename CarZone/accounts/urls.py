from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

from .views import SignUpUserView, SignInUserView, logout_then_login, index, UpdateUserView, deactivate

urlpatterns: tuple = (
    path('', RedirectView.as_view(pattern_name='login')),
    path('accounts/', include(
        [
            path('login/', SignInUserView.as_view(), name='login'),
            path('sign-up/', SignUpUserView.as_view(), name='sign-up'),
            path('logout/', logout_then_login, name='logout'),
            path('profile/', UpdateUserView.as_view(), name='profile'),
            path('posts/', index, name='user_posts'),
            path('deactivate/', include(
                [
                    path(
                        'confirm/',
                        TemplateView.as_view(template_name='accounts/deactivation-confirm.html'),
                        name='deactivate-confirm'
                    ),
                    path('', deactivate, name='deactivate-account')
                ]
            )),
        ]
    )),
)
