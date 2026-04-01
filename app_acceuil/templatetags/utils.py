from django import template
from django.utils.text import slugify

register = template.Library()


@register.filter(name="prefix")
def prefix(value):
    """
    Extract the prefix (first part before underscore) from a URL name.
    For example: 'blogue_list' -> 'blogue', 'projet_detail' -> 'projet'
    """
    if value:
        return value.split("_")[0]
    return value


@register.filter(name="extract_year")
def extract_year(value):
    """
    Extrait l'annee ou la plage d'annees a la fin d'un texte apres une virgule.
    Ex: "Nordikeau, 2022" -> "2022"
    """
    if not value or "," not in value:
        return ""

    parts = value.split(",")
    return parts[-1].strip()


@register.filter(name="remove_year")
def remove_year(value):
    """
    Retire l'annee de la fin du texte.
    Ex: "Nordikeau, 2022" -> "Nordikeau"
    """
    if not value or "," not in value:
        return value

    parts = value.rsplit(",", 1)
    return parts[0].strip()


@register.simple_tag
def profile_url_params(profile):
    """
    Genere les parametres d'URL pour un profil dans le chemin.
    Retourne: nom=youssoupha-marega&profession=scientifique-de-donnees
    """
    if not profile or profile.is_default:
        return ""

    nom_slug = slugify(f"{profile.first_name}-{profile.last_name}")
    profession_slug = slugify(profile.profession) if profile.profession else "profil"
    return f"nom={nom_slug}&profession={profession_slug}"


@register.filter(name="profile_nom_slug")
def profile_nom_slug(profile):
    """
    Genere le slug du nom complet pour les URLs de profil.
    """
    if not profile:
        return ""
    return slugify(f"{profile.first_name}-{profile.last_name}")


@register.filter(name="profile_profession_slug")
def profile_profession_slug(profile):
    """
    Genere le slug de la profession pour les URLs de profil.
    """
    if not profile or not profile.profession:
        return "profil"
    return slugify(profile.profession)


@register.filter(name="split_csv")
def split_csv(value):
    """
    Decoupe une chaine separee par des virgules en liste nettoyee.
    Ex: "Python, Docker, FastAPI" -> ["Python", "Docker", "FastAPI"]
    """
    if not value:
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]


@register.filter(name="project_stack_items")
def project_stack_items(value):
    """
    Retourne les stacks inline d'un contenu si elles existent.
    """
    if hasattr(value, "stack_items"):
        return list(value.stack_items.all())
    return []


@register.filter(name="content_stack_items")
def content_stack_items(value):
    return project_stack_items(value)
