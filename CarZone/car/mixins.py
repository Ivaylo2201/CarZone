from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse


class AvailabilityRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs) -> HttpResponseRedirect:
        if not self.get_object().is_available:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnershipRequiredMixin(AccessMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if self.request.user.pk != self.get_object().dealer.pk:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
