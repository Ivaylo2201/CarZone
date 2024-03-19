from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Sum, QuerySet
from django.contrib.auth import login, logout, get_user_model
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from .forms import CarZoneUserCreationForm, CarZoneAuthenticationForm, CarZoneUserUpdateForm

UserModel = get_user_model()


def initial(request: HttpRequest) -> HttpResponseRedirect:
    return logout_then_login(request)


class DeactivationConfirmTemplateView(TemplateView):
    template_name = 'accounts/deactivation-confirm.html'


class SignUpUserView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = CarZoneUserCreationForm
    success_url = reverse_lazy('profile')


    def form_valid(self, form) -> HttpResponse:
        result: HttpResponse = super().form_valid(form)
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
        posts: QuerySet = self.get_object().posts.filter(is_available=True)

        statistics: dict = (
            posts.aggregate(
                total_price=Sum('price'),
                total_views=Sum('views'),
            )
        )

        context['posts'] = posts.count()
        context['total_price'] = statistics['total_price'] or 0
        context['total_views'] = statistics['total_views'] or 0

        return context


def logout_then_login(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)

    return redirect('login')


def deactivate(request: HttpRequest) -> HttpResponseRedirect:
    request.user.is_active = False
    request.user.save()

    return logout_then_login(request)
