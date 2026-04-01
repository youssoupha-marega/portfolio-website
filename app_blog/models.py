from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from app_acceuil.base_models import PublishableContent, PublishableContentManager


class BlogPost(PublishableContent):
    """
    Modele pour les articles de blog.
    """

    content = RichTextUploadingField(verbose_name="Contenu de l'article")
    main_image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
        verbose_name="Image principale",
    )
    github_url = models.URLField(blank=True, verbose_name="Lien GitHub")
    demo_url = models.URLField(blank=True, verbose_name="Lien demo")
    tags = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Tags (separes par des virgules)",
    )
    read_time = models.IntegerField(
        default=5,
        verbose_name="Temps de lecture (minutes)",
    )

    objects = PublishableContentManager()

    def get_absolute_url(self):
        return reverse("blogue_detail", kwargs={"slug": self.slug})

    class Meta(PublishableContent.Meta):
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"


class BlogPostStackItem(models.Model):
    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="stack_items",
        verbose_name="Article de blog",
    )
    name = models.CharField(max_length=100, verbose_name="Nom")
    icon = models.ImageField(
        upload_to="blog_stack/",
        blank=True,
        null=True,
        verbose_name="Logo",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ("order", "id")
        verbose_name = "Stack blog"
        verbose_name_plural = "Stacks blog"

    def __str__(self):
        return f"{self.blog_post.title} - {self.name}"
