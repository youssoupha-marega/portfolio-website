from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from app_acceuil.base_models import PublishableContent, PublishableContentManager


class Project(PublishableContent):
    """
    Modele pour les projets du portfolio.
    """

    content = RichTextUploadingField(verbose_name="Contenu detaille")
    main_image = models.ImageField(
        upload_to="projets/",
        blank=True,
        null=True,
        verbose_name="Image principale",
    )
    github_url = models.URLField(blank=True, verbose_name="Lien GitHub")
    demo_url = models.URLField(blank=True, verbose_name="Lien demo")

    objects = PublishableContentManager()

    def get_absolute_url(self):
        return reverse("projet_detail", kwargs={"slug": self.slug})

    class Meta(PublishableContent.Meta):
        verbose_name = "Projet"
        verbose_name_plural = "Projets"


class ProjectStackItem(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="stack_items",
        verbose_name="Projet",
    )
    name = models.CharField(max_length=100, verbose_name="Nom")
    icon = models.ImageField(
        upload_to="project_stack/",
        blank=True,
        null=True,
        verbose_name="Logo",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ("order", "id")
        verbose_name = "Stack projet"
        verbose_name_plural = "Stacks projet"

    def __str__(self):
        return f"{self.project.title} - {self.name}"
