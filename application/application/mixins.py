from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class AnonymityRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main_page')
        return super().dispatch(request, *args, **kwargs)
    

class AuthorizationRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    