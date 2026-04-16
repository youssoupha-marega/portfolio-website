"""
Modeles de base abstraits pour partager la logique commune entre
Project, BlogPost et Service.
"""

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField


class PublishableContent(models.Model):
    """
    Modele abstrait pour tout contenu publiable.
    """

    title = models.CharField(max_length=200, verbose_name=_("Titre"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Slug"))
    resume = RichTextUploadingField(verbose_name=_("Résumé"))

    author_name = models.CharField(
        max_length=100,
        verbose_name=_("Nom de l'auteur"),
        default="Youssoupha Marega",
    )
    author_email = models.EmailField(
        verbose_name=_("Email de l'auteur"),
        default="contact@youssouphamarega.com",
    )
    author_profession = models.CharField(
        max_length=100,
        verbose_name=_("Profession de l'auteur"),
        default="Data Scientist",
    )

    stack = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Stack technique"),
    )
    domaine = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Domaine"),
    )

    STATUS_CHOICES = [
        ("disponible", _("Disponible")),
        ("bientot_disponible", _("Bientôt disponible")),
        ("complet", _("Complet")),
        ("planning", _("En planification")),
        ("in_progress", _("En cours")),
        ("paused", _("En pause")),
        ("deployed", _("Déployé")),
        ("completed", _("Terminé")),
        ("archived", _("Archivé")),
    ]
    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        default="",
        verbose_name=_("Statut"),
    )

    afficher_liste = models.BooleanField(
        default=True,
        verbose_name=_("Afficher dans la liste"),
    )
    afficher_detail = models.BooleanField(
        default=True,
        verbose_name=_("Afficher la page de détail"),
    )

    published_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de publication"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))

    class Meta:
        abstract = True
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class PublishableContentManager(models.Manager):
    def all_items(self):
        return self.all()

    def get_by_slug(self, slug):
        return self.get(slug=slug)
