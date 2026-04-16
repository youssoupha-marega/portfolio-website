from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from django.forms import inlineformset_factory
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import SiteProfile, Section, SectionItem


class SectionItemForm(forms.ModelForm):
	details = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label="Détails (affichés via icône œil)")
	
	class Meta:
		model = SectionItem
		fields = ["title", "subtitle", "date", "url", "icon", "order", "details"]


class SectionItemInline(admin.StackedInline):
	model = SectionItem
	form = SectionItemForm
	extra = 1
	can_delete = True
	fields = [("title", "date"), ("subtitle", "url"), ("icon", "order"), "details"]
	verbose_name = "Sous-section / Item"
	verbose_name_plural = "Sous-sections / Items (Compétences, Formations, Expériences, etc.)"


class SectionInline(admin.StackedInline):
	model = Section
	extra = 0
	can_delete = True
	fields = ("title", "section_type", "is_active", "order", "items_inline")
	readonly_fields = ("items_inline",)
	classes = ("collapse",)
	
	def items_inline(self, obj):
		"""Affiche un formulaire inline pour les items de cette section"""
		if not obj or not obj.pk:
			return "Sauvegardez d'abord la section pour ajouter des sous-sections."
		
		items = obj.items.all().order_by('order')
		
		if not items.exists():
			html = '<p style="color:#666;font-style:italic;">Aucune sous-section. Cliquez sur "Modifier cette section" ci-dessous pour en ajouter.</p>'
		else:
			html = '<div style="background:#f9f9f9;padding:10px;border-radius:5px;margin:10px 0;">'
			html += '<table style="width:100%;border-collapse:collapse;">'
			html += '<tr style="background:#e0e0e0;"><th style="padding:8px;text-align:left;">Titre</th><th style="padding:8px;text-align:left;">Sous-titre</th><th style="padding:8px;text-align:center;">Ordre</th></tr>'
			for item in items:
				html += f'<tr style="border-bottom:1px solid #ddd;">'
				html += f'<td style="padding:8px;"><strong>{item.title}</strong></td>'
				html += f'<td style="padding:8px;">{item.subtitle or "-"}</td>'
				html += f'<td style="padding:8px;text-align:center;">{item.order}</td>'
				html += f'</tr>'
			html += '</table></div>'
		
		edit_url = f'/admin/app_acceuil/section/{obj.pk}/change/'
		html += f'<a href="{edit_url}" class="button" style="margin-top:10px;display:inline-block;">✏️ Modifier cette section et ses sous-sections</a>'
		
		return mark_safe(html)
	
	items_inline.short_description = "Sous-sections / Compétences"


# Admin pour Section (accessible via le lien depuis SiteProfile)
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
	inlines = [SectionItemInline]
	list_display = ("title", "section_type", "profile", "is_active", "order")
	list_filter = ("profile", "section_type", "is_active")
	list_editable = ("is_active", "order")
	search_fields = ("title", "profile__first_name", "profile__last_name")
	fields = ("profile", "title", "title_image", "section_type", "is_active", "order")


class SiteProfileForm(forms.ModelForm):
	bio = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
	projects_home_intro = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label="Texte d'introduction Projets (Accueil)")
	projects_page_intro = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label="Texte d'introduction page Projets")
	blog_home_intro = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label="Texte d'introduction Blog (Accueil)")
	blog_page_intro = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label="Texte d'introduction page Blog")
	services_home_intro = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label="Texte d'introduction Services (Accueil)")
	services_page_intro = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label="Texte d'introduction page Services")

	class Meta:
		model = SiteProfile
		fields = "__all__"


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
	form = SiteProfileForm
	inlines = [SectionInline]
	list_display = ("first_name", "last_name", "profession", "slug_url_display", "is_published", "is_default", "profile_preview")
	list_editable = ("is_published", "is_default",)
	list_filter = ("is_published", "is_default",)
	readonly_fields = ("profile_preview", "slug", "profile_url_display")
	search_fields = ("first_name", "last_name", "profession", "email")
	filter_horizontal = ("published_projects", "featured_projects", "published_articles", "featured_articles", "published_services", "featured_services")

	fieldsets = (
		("Publication", {"fields": ("is_published", "is_default", "slug", "profile_url_display"), "classes": ("collapse",)} ),
		(None, {"fields": ("first_name", "last_name", "email", "profile_photo", "profile_preview")} ),
		("Infos professionnelles", {"fields": ("profession", "current_employer", "current_employer_url"), "classes": ("collapse",)} ),
		("Liens", {"fields": ("linkedin_url", "github_url", "medium_url", "youtube_url"), "classes": ("collapse",)} ),
		("Localisation & Bio", {"fields": ("location", "bio"), "classes": ("collapse",)} ),
		("Affichage Profil (position/titre/image)", {"fields": ("bio_is_active", "bio_position", "bio_show_title", "bio_title", "bio_title_image"), "classes": ("collapse",)} ),
		("Projets publiés", {"fields": ("published_projects", "featured_projects"), "classes": ("collapse",)} ),
		("Articles publiés", {"fields": ("published_articles", "featured_articles"), "classes": ("collapse",)} ),
		("Services publiés", {"fields": ("published_services", "featured_services"), "classes": ("collapse",)} ),
		("Section Projets (titres/textes/images)", {"fields": ("projects_display_order", "projects_home_title", "projects_home_intro", "projects_home_image", "projects_navbar_label", "projects_page_title", "projects_page_intro", "projects_page_image", "projects_view_all_text", "projects_detail_button_text", "projects_back_button_text"), "classes": ("collapse",)} ),
		("Section Projets - Métadonnées (Matrice 4×3)", {"fields": (("projects_show_author_home", "projects_show_author_list", "projects_show_author_detail"), ("projects_show_profession_home", "projects_show_profession_list", "projects_show_profession_detail"), ("projects_show_publish_date_home", "projects_show_publish_date_list", "projects_show_publish_date_detail"), ("projects_show_update_date_home", "projects_show_update_date_list", "projects_show_update_date_detail")), "description": "Colonnes: Accueil | Liste | Détails", "classes": ("collapse",)} ),
		("Section Blog (titres/textes/images)", {"fields": ("blog_display_order", "blog_home_title", "blog_home_intro", "blog_home_image", "blog_navbar_label", "blog_page_title", "blog_page_intro", "blog_page_image", "blog_view_all_text", "blog_detail_button_text", "blog_back_button_text"), "classes": ("collapse",)} ),
		("Section Blog - Métadonnées (Matrice 4×3)", {"fields": (("blog_show_author_home", "blog_show_author_list", "blog_show_author_detail"), ("blog_show_profession_home", "blog_show_profession_list", "blog_show_profession_detail"), ("blog_show_publish_date_home", "blog_show_publish_date_list", "blog_show_publish_date_detail"), ("blog_show_update_date_home", "blog_show_update_date_list", "blog_show_update_date_detail")), "description": "Colonnes: Accueil | Liste | Détails", "classes": ("collapse",)} ),
		("Visibilite des pages Services", {"fields": ("services_page_enabled",), "description": "Decocher pour desactiver les pages /services/ et /services/<slug>/. La navbar et les boutons renverront vers la section #services de l'accueil.", "classes": ("collapse",)} ),
		("Section Services (titres/textes/images)", {"fields": ("services_display_order", "services_home_title", "services_home_intro", "services_home_image", "services_navbar_label", "services_page_title", "services_page_intro", "services_page_image", "services_view_all_text", "services_detail_button_text", "services_back_button_text", "services_calendly_button_text"), "classes": ("collapse",)} ),
		("Section Services - Métadonnées (Matrice 4×3)", {"fields": (("services_show_author_home", "services_show_author_list", "services_show_author_detail"), ("services_show_profession_home", "services_show_profession_list", "services_show_profession_detail"), ("services_show_publish_date_home", "services_show_publish_date_list", "services_show_publish_date_detail"), ("services_show_update_date_home", "services_show_update_date_list", "services_show_update_date_detail")), "description": "Colonnes: Accueil | Liste | Détails", "classes": ("collapse",)} ),
		("Section Contact (formulaire)", {"fields": ("contact_display_order", "contact_title", "contact_title_image", "contact_intro_text", "contact_name_label", "contact_email_label", "contact_company_label", "contact_profession_label", "contact_subject_label", "contact_message_label", "contact_button_text", "contact_success_message", "contact_error_message", "enable_confirmation_email", "gmail_app_password"), "classes": ("collapse",)} ),
		("Branding", {"fields": ("site_title", "favicon", "navbar_position", "navbar_avatar_shape", "navbar_avatar"), "classes": ("collapse",)} ),
	)

	def profile_preview(self, obj):
		if obj and obj.profile_photo:
			return mark_safe(f"<img src='{obj.profile_photo.url}' style='max-height:120px;border-radius:8px;' />")
		return "-"

	profile_preview.short_description = "Aperçu photo"
	
	def slug_url_display(self, obj):
		"""Affiche l'URL complète du profil dans la liste"""
		if not obj:
			return "-"
		
		if obj.is_default:
			return "/"
		else:
			from django.utils.text import slugify
			nom_slug = slugify(f"{obj.first_name}-{obj.last_name}") if obj.first_name and obj.last_name else "prenom-nom"
			profession_slug = slugify(obj.profession) if obj.profession else "profession"
			return f"/profil/nom={nom_slug}&profession={profession_slug}/"
	
	slug_url_display.short_description = "SLUG URL"
	
	def profile_url_display(self, obj):
		"""Affiche l'URL complète du profil"""
		if not obj:
			return "-"
		
		if obj.is_default:
			url_text = "/"
			description = "Profil par défaut (racine)"
		else:
			from django.utils.text import slugify
			nom_slug = slugify(f"{obj.first_name}-{obj.last_name}") if obj.first_name and obj.last_name else "nom-prenom"
			profession_slug = slugify(obj.profession) if obj.profession else "profession"
			url_text = f"/profil/nom={nom_slug}&profession={profession_slug}/"
			description = "URL du profil"
		
		return mark_safe(f'<div style="padding:10px;background:#f0f0f0;border-radius:4px;font-family:monospace;">'
						f'<strong style="color:#0066cc;">{description}:</strong><br>'
						f'<span style="font-size:13px;color:#333;">{url_text}</span></div>')
	
	profile_url_display.short_description = "URL du profil"


# Les modèles Education, Experience, Section et SectionItem sont gérés uniquement via les inlines dans SiteProfile
# Ils n'apparaissent pas comme sections séparées dans l'admin