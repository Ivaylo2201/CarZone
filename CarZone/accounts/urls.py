from django.urls import path, include
from django.views.generic import RedirectView

from .views import SignUpUserView, SignInUserView, logout_then_login, index

urlpatterns: tuple = (
    path('', RedirectView.as_view(pattern_name='login')),
    path('accounts/', include(
        [
            path('login/', SignInUserView.as_view(), name='login'),
            path('sign-up/', SignUpUserView.as_view(), name='sign-up'),
            path('logout/', logout_then_login, name='logout'),
            path('<int:pk>', include(
                [
                    path('', index, name='user'),
                    path('update/', index, name='user_update'),
                    path('posts/', index, name='user_posts')
                ]
            )),
        ]
    )),
)
