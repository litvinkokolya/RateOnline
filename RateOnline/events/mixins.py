from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class PhotoRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.image:
            return redirect(reverse_lazy('photo_selection'))
        return super().dispatch(request, *args, **kwargs)
