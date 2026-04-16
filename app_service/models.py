from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from app_acceuil.base_models import PublishableContent, PublishableContentManager


class Service(PublishableContent):
    """
    Modèle pour les services proposés.
    
    Hérite de PublishableContent pour les champs communs (title, slug, resume,
    is_published, featured, author_*, dates, etc.).
    
    Ajoute uniquement les champs spécifiques aux services.
    """
    
    # Champs spécifiques aux services
    content = RichTextUploadingField(verbose_name="Description complète du service")
    calendly_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Lien Calendly pour réservation"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Prix (optionnel)"
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Durée de session (ex: '1 heure', '2 jours')"
    )
    duree = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Durée estimée du projet (ex: '4–8 semaines')"
    )
    localisation = models.CharField(
        max_length=200,
        blank=True,
        default="Remote / Montréal",
        verbose_name="Localisation"
    )
    livrables_label = models.CharField(
        max_length=100,
        blank=True,
        default="Livrables",
        verbose_name="Titre de la section livrables (ex: 'Livrables', 'Modules')"
    )

    objects = PublishableContentManager()

    def get_absolute_url(self):
        """Retourne l'URL de la page de détail du service."""
        return reverse('service_detail', kwargs={'slug': self.slug})

    class Meta(PublishableContent.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"
        # Hérite ordering = ['-created_at'] de PublishableContent


class Livrable(models.Model):
    """Élément de livrable lié à un service."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="livrables",
        verbose_name="Service",
    )
    contenu = models.CharField(max_length=500, verbose_name="Contenu")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ("ordre", "id")
        verbose_name = "Livrable"
        verbose_name_plural = "Livrables"

    def __str__(self):
        return f"{self.service.title} — {self.contenu[:60]}"
