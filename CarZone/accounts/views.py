from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView

from .forms import CarZoneUserCreationForm, CarZoneAuthenticationForm, CarZoneUserUpdateForm

UserModel = get_user_model()


def initial(request: HttpRequest) -> HttpResponseRedirect:
    print(f'Currently logged: {request.user.username}')
    return logout_then_login(request)


class DeactivationConfirmTemplateView(TemplateView):
    template_name = 'accounts/deactivation-confirm.html'


class SignUpUserView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = CarZoneUserCreationForm
    success_url = reverse_lazy('catalogue')


    def form_valid(self, form) -> HttpResponseRedirect:
        result = super().form_valid(form)
        login(self.request, form.instance)
        return result


class SignInUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CarZoneAuthenticationForm


    def get_success_url(self) -> str:
        return reverse('catalogue')


class UpdateUserView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    form_class = CarZoneUserUpdateForm
    success_url = reverse_lazy('profile')


    def get_object(self, queryset=None) -> UserModel:
        return self.request.user


    def get_context_data(self, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)
        posts = self.get_object().posts.filter(is_available=True)

        statistics: dict = (
            posts.aggregate(
                total_price=Sum('price'),
                total_views=Sum('views')
            )
        )

        context['posts'] = posts.count()
        context['total_price'] = statistics.get('total_price', 0)
        context['total_views'] = statistics['total_views'] or 0

        return context


def logout_then_login(request: HttpRequest) -> HttpResponseRedirect:
    print(f'Logging out {request.user.username}...')
    logout(request)
    return redirect('login')


def deactivate(request: HttpRequest) -> HttpResponseRedirect:
    print(f"Deactivating {request.user.username}'s account...")
    request.user.is_active = False
    request.user.save()
    return logout_then_login(request)
