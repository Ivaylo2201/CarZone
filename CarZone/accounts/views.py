from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import CarZoneUserCreationForm, CarZoneAuthenticationForm


def index(request):
    return HttpResponse('test')


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


def logout_then_login(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect('login')
