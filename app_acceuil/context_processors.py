# app_acceuil/context_processors.py
from .models import SiteProfile
from django.db import DatabaseError, OperationalError


def menu_items(request):
    """Generate dynamic menu items based on the current profile"""
    try:
        # Essayer de détecter le profil depuis les paramètres du chemin
        nom = None
        profession = None
        if request.resolver_match:
            nom = request.resolver_match.kwargs.get('nom')
            profession = request.resolver_match.kwargs.get('profession')
        
        profile_slug = f"{nom}-{profession}" if nom and profession else None
        
        if profile_slug:
            # Profil spécifique
            profile = SiteProfile.objects.filter(slug=profile_slug, is_published=True).first()
        else:
            # Profil par défaut
            profile = SiteProfile.objects.filter(is_default=True, is_published=True).first()
        
        if profile:
            projects_label = profile.projects_navbar_label if profile.projects_navbar_label else "Projets"
            blog_label = profile.blog_navbar_label if profile.blog_navbar_label else "Blogue"
            services_label = profile.services_navbar_label if profile.services_navbar_label else "Services"
            
            # Récupérer l'ordre des sections (seulement celles dans la navbar)
            ordered_sections = [s for s in profile.get_ordered_sections() if s['in_navbar']]
            
            # Mapping des types de sections vers leurs configurations
            section_config = {
                'projects': {'name': 'projet_list', 'profile_name': 'profile_projet_list', 'label': projects_label, 'default_path': '/projets/', 'profile_path': '/projets/'},
                'blog': {'name': 'blogue_list', 'profile_name': 'profile_blogue_list', 'label': blog_label, 'default_path': '/blogue/', 'profile_path': '/blog/'},
                'services': {'name': 'service_list', 'profile_name': 'profile_service_list', 'label': services_label, 'default_path': '/services/', 'profile_path': '/services/'},
            }
            
            # Générer les URLs en fonction du profil
            if profile.is_default:
                items = [{"name": "acceuil", "label": "Accueil", "url": "/"}]
                for section in ordered_sections:
                    config = section_config[section['type']]
                    # Services : pointer vers #services si les pages sont désactivées
                    if section['type'] == 'services' and not getattr(profile, 'services_page_enabled', True):
                        url = "/#services"
                    else:
                        url = config['default_path']
                    items.append({"name": config['name'], "label": config['label'], "url": url})
            else:
                # Utiliser les paramètres dans le chemin
                from django.utils.text import slugify
                nom_slug = slugify(f"{profile.first_name}-{profile.last_name}")
                profession_slug = slugify(profile.profession) if profile.profession else "profil"
                base_path = f"/profil/nom={nom_slug}&profession={profession_slug}"

                items = [{"name": "profile_home", "label": "Accueil", "url": f"{base_path}/"}]
                for section in ordered_sections:
                    config = section_config[section['type']]
                    # Services : pointer vers la section d'accueil si les pages sont désactivées
                    if section['type'] == 'services' and not getattr(profile, 'services_page_enabled', True):
                        url = f"{base_path}/#services"
                    else:
                        url = f"{base_path}{config['profile_path']}"
                    items.append({"name": config['profile_name'], "label": config['label'], "url": url})
        else:
            items = [
                {"name": "acceuil", "label": "Accueil", "url": "/"},
                {"name": "service_list", "label": "Services", "url": "/services/"},
                {"name": "projet_list", "label": "Projets", "url": "/projets/"},
                {"name": "blogue_list", "label": "Blogue", "url": "/blogue/"},
            ]
    except (OperationalError, DatabaseError):
        items = [
            {"name": "acceuil", "label": "Accueil", "url": "/"},
            {"name": "service_list", "label": "Services", "url": "/services/"},
            {"name": "projet_list", "label": "Projets", "url": "/projets/"},
            {"name": "blogue_list", "label": "Blogue", "url": "/blogue/"},
        ]
    
    return {'menu_items': items}


def site_profile(request):
    """Expose the current SiteProfile instance as `site_profile` in templates.

    This context processor is defensive: during initial migrations the
    `app_acceuil_siteprofile` table or new columns (like `site_title`) may
    not exist yet which leads to OperationalError. Catch DB errors and
    return `None` so templates can still render (they already have fallbacks).
    """
    try:
        # Essayer de détecter le profil depuis les paramètres du chemin
        nom = None
        profession = None
        if request.resolver_match:
            nom = request.resolver_match.kwargs.get('nom')
            profession = request.resolver_match.kwargs.get('profession')
        
        profile_slug = f"{nom}-{profession}" if nom and profession else None
        
        if profile_slug:
            # Profil spécifique
            profile = SiteProfile.objects.filter(slug=profile_slug, is_published=True).first()
        else:
            # Profil par défaut
            profile = SiteProfile.objects.filter(is_default=True, is_published=True).first()
    except (OperationalError, DatabaseError):
        # Database not ready / migrations not applied yet. Return no profile.
        profile = None
    return {"site_profile": profile}
