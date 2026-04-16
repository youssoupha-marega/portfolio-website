"""
Vues génériques de base pour partager la logique commune entre
les apps projet, blog et service.
"""

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from app_acceuil.models import SiteProfile


@method_decorator(never_cache, name='dispatch')
class ProfileBasedListView(ListView):
    """
    Vue de liste de base pour afficher du contenu lié à un profil.
    
    Les sous-classes doivent définir :
    - model: Le modèle à lister (Project, BlogPost, Service)
    - template_name: Le template à utiliser
    - context_object_name: Le nom de la liste dans le contexte
    - profile_featured_attr: L'attribut du profil pour le contenu featured (ex: 'featured_projects')
    """
    
    paginate_by = 9
    profile_featured_attr = None  # À définir dans les sous-classes
    
    def get_queryset(self):
        """Récupère le queryset filtré pour le profil actuel."""
        # Si on a un profil spécifique, utiliser ses contenus
        profile = self.get_profile()
        if profile and self.profile_featured_attr:
            # Utiliser les contenus associés au profil via ManyToMany
            profile_content = getattr(profile, self.profile_featured_attr, None)
            if profile_content and profile_content.exists():
                return profile_content.filter(afficher_liste=True)

        # Fallback: retourner tous les items visibles en liste
        return super().get_queryset().filter(afficher_liste=True)
    
    def get_profile(self):
        """Récupère le profil depuis les paramètres d'URL ou le profil par défaut."""
        nom = self.kwargs.get('nom')
        profession = self.kwargs.get('profession')
        
        if nom and profession:
            profile_slug = f"{nom}-{profession}"
            return get_object_or_404(
                SiteProfile.objects.get_published_with_content(),
                slug=profile_slug
            )
        else:
            return SiteProfile.objects.get_default_profile()
    
    def get_context_data(self, **kwargs):
        """Ajoute le profil au contexte."""
        context = super().get_context_data(**kwargs)
        context['site_profile'] = self.get_profile()
        return context


@method_decorator(never_cache, name='dispatch')
class ProfileBasedDetailView(DetailView):
    """
    Vue de détail de base pour afficher un élément de contenu.
    
    Les sous-classes doivent définir :
    - model: Le modèle à afficher (Project, BlogPost, Service)
    - template_name: Le template à utiliser
    - context_object_name: Le nom de l'objet dans le contexte
    """
    
    def get_queryset(self):
        """Récupère le contenu du modèle."""
        return super().get_queryset().all()

    def get_object(self, queryset=None):
        """Retourne 404 si afficher_detail est False."""
        obj = super().get_object(queryset)
        if not obj.afficher_detail:
            raise Http404
        return obj
    
    def get_profile(self):
        """Récupère le profil depuis les paramètres d'URL ou le profil par défaut."""
        nom = self.kwargs.get('nom')
        profession = self.kwargs.get('profession')
        
        if nom and profession:
            profile_slug = f"{nom}-{profession}"
            return get_object_or_404(
                SiteProfile.objects.get_published_with_content(),
                slug=profile_slug
            )
        else:
            return SiteProfile.objects.get_default_profile()
    
    def get_context_data(self, **kwargs):
        """Ajoute le profil au contexte."""
        context = super().get_context_data(**kwargs)
        context['site_profile'] = self.get_profile()
        return context
