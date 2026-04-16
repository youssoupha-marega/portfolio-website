from django import forms
from django.contrib import admin

from .models import BlogPost, BlogPostStackItem


class BlogPostStackItemInline(admin.TabularInline):
    model = BlogPostStackItem
    extra = 1
    fields = ("name", "icon", "order")
    verbose_name = "Technologie"
    verbose_name_plural = "Technologies / Logos de stack"


class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = "__all__"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    inlines = [BlogPostStackItemInline]
    list_display = ("title", "statut", "afficher_liste", "afficher_detail", "author_name", "published_at", "updated_at")
    list_filter = ("published_at", "author_name", "statut", "afficher_liste", "afficher_detail")
    search_fields = ("title", "resume", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)

    fieldsets = (
        (
            "Informations principales",
            {
                "fields": ("title", "slug", "resume", "domaine", "statut"),
                "description": "Ajoute ensuite les technologies et leurs logos dans le tableau inline plus bas.",
            },
        ),
        ("Contenu", {"fields": ("content", "main_image")}),
        ("Liens", {"fields": ("github_url", "demo_url")}),
        ("Auteur", {"fields": ("author_name", "author_email", "author_profession")}),
        (
            "Visibilité",
            {
                "fields": ("afficher_liste", "afficher_detail"),
                "description": (
                    '"Afficher dans la liste" : contrôle l\'apparition dans /blog/. '
                    '"Afficher la page de détail" : si décoché, /blog/<slug>/ retourne une 404.'
                ),
            },
        ),
        (
            "Dates",
            {
                "fields": ("published_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        return self.prepopulated_fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("slug", "created_at", "updated_at", "published_at")
        return ("created_at", "updated_at", "published_at")
