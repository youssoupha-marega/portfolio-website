from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Service, Livrable


class ServiceForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label="Description complète du service")

    class Meta:
        model = Service
        fields = '__all__'


class LivrableInline(admin.TabularInline):
    model = Livrable
    extra = 1
    fields = ("contenu", "ordre")
    verbose_name = "Livrable"
    verbose_name_plural = "Livrables (affichés sur la carte service)"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceForm
    inlines = [LivrableInline]
    list_display = ('title', 'statut', 'afficher_liste', 'afficher_detail', 'author_name', 'published_at', 'updated_at')
    list_filter = ('published_at', 'author_name', 'afficher_liste', 'afficher_detail')
    search_fields = ('title', 'resume', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)

    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'slug', 'resume', 'domaine', 'statut')
        }),
        ('Contenu', {
            'fields': ('content',)
        }),
        ('Détails du service', {
            'fields': ('duree', 'localisation', 'livrables_label', 'price', 'duration', 'calendly_url'),
            'description': 'Ajoutez ensuite les livrables dans le tableau inline plus bas.'
        }),
        ('Auteur', {
            'fields': ('author_name', 'author_email', 'author_profession')
        }),
        ('Visibilité', {
            'fields': ('afficher_liste', 'afficher_detail'),
            'description': (
                '"Afficher dans la liste" : contrôle l\'apparition dans /services/. '
                '"Afficher la page de détail" : si décoché, /services/<slug>/ retourne une 404.'
            ),
        }),
        ('Dates', {
            'fields': ('published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        return self.prepopulated_fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('slug', 'created_at', 'updated_at', 'published_at')
        return ('created_at', 'updated_at', 'published_at')
