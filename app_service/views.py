"""
Vues pour l'application services.

Utilise les classes de base ProfileBasedListView et ProfileBasedDetailView
pour éliminer la duplication de code.
"""

from django.http import Http404
from app_acceuil.base_views import ProfileBasedListView, ProfileBasedDetailView
from .models import Service


class ServiceListView(ProfileBasedListView):
    """Vue de liste des services pour un profil."""

    model = Service
    template_name = 'app_service/list.html'
    context_object_name = 'services'
    profile_featured_attr = 'published_services'

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_profile()
        if profile and not getattr(profile, 'services_page_enabled', True):
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ServiceDetailView(ProfileBasedDetailView):
    """Vue de détail d'un service."""

    model = Service
    template_name = 'app_service/detail.html'
    context_object_name = 'service'

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_profile()
        if profile and not getattr(profile, 'services_page_enabled', True):
            raise Http404
        return super().dispatch(request, *args, **kwargs)


# Vues fonctionnelles pour compatibilité avec les URLs existantes
def service_list(request, nom=None, profession=None):
    """Wrapper fonctionnel pour ServiceListView."""
    view = ServiceListView.as_view()
    return view(request, nom=nom, profession=profession)


def service_detail(request, slug, nom=None, profession=None):
    """Wrapper fonctionnel pour ServiceDetailView."""
    view = ServiceDetailView.as_view()
    return view(request, slug=slug, nom=nom, profession=profession)
