from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField


class SiteProfileManager(models.Manager):
	"""Custom manager for SiteProfile with optimized queries."""
	
	def get_published_with_content(self):
		"""
		Get published profiles with all related content prefetched.
		
		Returns:
			QuerySet: Optimized queryset with prefetch_related for all M2M relationships.
		"""
		return self.prefetch_related(
			'sections__items',
			'featured_projects', 'published_projects',
			'featured_articles', 'published_articles',
			'featured_services', 'published_services'
		).filter(is_published=True)
	
	def get_default_profile(self):
		"""
		Get the default profile (is_default=True) with all content.
		
		Returns:
			SiteProfile or None: The default profile if exists, None otherwise.
		"""
		return self.get_published_with_content().filter(is_default=True).first()
	
	def get_by_slug_with_content(self, slug):
		"""
		Get a specific profile by slug with all content prefetched.
		
		Args:
			slug (str): The profile slug.
			
		Returns:
			SiteProfile: The profile instance.
			
		Raises:
			SiteProfile.DoesNotExist: If no profile with this slug exists.
		"""
		return self.get_published_with_content().get(slug=slug)


class SiteProfile(models.Model):
	"""
	Model to hold the public profile / account information shown on the site.
	
	Attributes:
		is_default: If True, this profile is displayed at the root URL (/).
		is_published: If True, this profile is publicly visible.
		slug: Auto-generated URL slug (format: firstname-lastname-profession).
	"""
	is_default = models.BooleanField(default=False, verbose_name=_("Profil par défaut (racine /)"))
	is_published = models.BooleanField(default=False, verbose_name=_("Publier ce profil"))
	slug = models.SlugField(max_length=255, unique=True, verbose_name=_("Slug URL"), help_text=_("URL unique pour ce profil (ex: youssoupha-marega-data-scientist)"))
	
	objects = SiteProfileManager()
	
	first_name = models.CharField(max_length=150, verbose_name=_("Prénom"))
	last_name = models.CharField(max_length=150, verbose_name=_("Nom"))
	location = models.CharField(max_length=255, blank=True, verbose_name=_("Localisation"))
	profession = models.CharField(max_length=255, blank=True, verbose_name=_("Profession"))
	current_employer = models.CharField(max_length=255, blank=True, verbose_name=_("Employeur actuel"))
	current_employer_url = models.URLField(blank=True, verbose_name=_("Lien employeur"))
	linkedin_url = models.URLField(blank=True, verbose_name=_("LinkedIn"))
	github_url = models.URLField(blank=True, verbose_name=_("GitHub"))
	email = models.EmailField(blank=True, verbose_name=_("Adresse email"))
	medium_url = models.URLField(blank=True, verbose_name=_("Medium"))
	youtube_url = models.URLField(blank=True, verbose_name=_("YouTube"))
	profile_photo = models.ImageField(upload_to="profile/", blank=True, null=True, verbose_name=_("Photo de profil"))
	bio = RichTextUploadingField(blank=True, verbose_name=_("Bio"))
	# Contrôles d'affichage de la section Profil
	BIO_POSITION_CHOICES = (("left", "Colonne gauche"), ("right", "Colonne droite"))
	bio_is_active = models.BooleanField(default=True, verbose_name=_("Afficher la carte Profil"))
	bio_position = models.CharField(max_length=10, choices=BIO_POSITION_CHOICES, default="right", verbose_name=_("Position de la section Profil"))
	bio_show_title = models.BooleanField(default=True, verbose_name=_("Afficher le titre de la section Profil"))
	bio_title = models.CharField(max_length=200, blank=True, verbose_name=_("Titre de la section Profil (facultatif)"))
	bio_title_image = models.ImageField(upload_to="section_images/", blank=True, null=True, verbose_name=_("Image du titre Bio"))

	# Branding fields for head/navbar editable in admin
	site_title = models.CharField(max_length=200, blank=True, verbose_name=_("Titre du site (balise <title>)"))
	favicon = models.ImageField(upload_to="favicon/", blank=True, null=True, verbose_name=_("Favicon"))
	NAVBAR_AVATAR_SHAPE = (("circle", "Circle"), ("square", "Square"), ("none", "No frame"))
	navbar_avatar_shape = models.CharField(max_length=10, choices=NAVBAR_AVATAR_SHAPE, default="circle", verbose_name=_("Forme avatar navbar"))
	# Optional separate avatar specifically for the navbar so admin can choose a different image
	navbar_avatar = models.ImageField(upload_to="navbar/", blank=True, null=True, verbose_name=_("Avatar navbar"))

	# Customizable Projects section titles and content
	projects_home_title = models.CharField(max_length=200, default="Projets mis en avant", verbose_name=_("Titre section Projets (Accueil)"))
	projects_home_intro = RichTextUploadingField(blank=True, verbose_name=_("Texte d'introduction Projets (Accueil)"))
	projects_navbar_label = models.CharField(max_length=100, default="Projets", verbose_name=_("Label navbar Projets"))
	projects_page_title = models.CharField(max_length=200, default="Mes Projets", verbose_name=_("Titre page liste Projets"))
	projects_page_intro = RichTextUploadingField(blank=True, verbose_name=_("Texte d'introduction page Projets"))
	projects_view_all_text = models.CharField(max_length=100, default="Voir tous les projets", verbose_name=_("Texte 'Voir tous les projets'"))
	projects_detail_button_text = models.CharField(max_length=100, default="Voir le projet", verbose_name=_("Texte bouton détail projet"))
	projects_back_button_text = models.CharField(max_length=100, default="Retour aux projets", verbose_name=_("Texte bouton retour projets"))

	# Customizable Blog section titles and content
	blog_home_title = models.CharField(max_length=200, default="Articles de blog mis en avant", verbose_name=_("Titre section Blog (Accueil)"))
	blog_home_intro = RichTextUploadingField(blank=True, verbose_name=_("Texte d'introduction Blog (Accueil)"))
	blog_navbar_label = models.CharField(max_length=100, default="Blogue", verbose_name=_("Label navbar Blog"))
	blog_page_title = models.CharField(max_length=200, default="Articles de blog", verbose_name=_("Titre page liste Blog"))
	blog_page_intro = RichTextUploadingField(blank=True, verbose_name=_("Texte d'introduction page Blog"))
	blog_view_all_text = models.CharField(max_length=100, default="Voir tous les articles", verbose_name=_("Texte 'Voir tous les articles'"))
	blog_detail_button_text = models.CharField(max_length=100, default="Lire l'article", verbose_name=_("Texte bouton lire article"))
	blog_back_button_text = models.CharField(max_length=100, default="Retour aux articles", verbose_name=_("Texte bouton retour articles"))

	# Customizable Services section titles and content
	services_home_title = models.CharField(max_length=200, default="Services", verbose_name=_("Titre section Services (Accueil)"))
	services_home_intro = RichTextUploadingField(blank=True, verbose_name=_("Texte d'introduction Services (Accueil)"))
	services_navbar_label = models.CharField(max_length=100, default="Services", verbose_name=_("Label navbar Services"))
	services_page_title = models.CharField(max_length=200, default="Services offerts", verbose_name=_("Titre page liste Services"))
	services_page_intro = RichTextUploadingField(blank=True, verbose_name=_("Texte d'introduction page Services"))
	services_view_all_text = models.CharField(max_length=100, default="Voir tous les services", verbose_name=_("Texte 'Voir tous les services'"))
	services_detail_button_text = models.CharField(max_length=100, default="En savoir plus", verbose_name=_("Texte bouton détail service"))
	services_back_button_text = models.CharField(max_length=100, default="Retour aux services", verbose_name=_("Texte bouton retour services"))
	services_calendly_button_text = models.CharField(max_length=100, default="Prendre rendez-vous", verbose_name=_("Texte bouton Calendly"))
	services_page_enabled = models.BooleanField(
		default=True,
		verbose_name=_("Pages liste et détail des services actives"),
		help_text=_(
			"Décocher pour désactiver les pages /services/ et /services/<slug>/. "
			"Le lien 'Services' dans la navbar et les boutons 'En savoir plus' renverront "
			"vers la section #services de la page d'accueil."
		),
	)

	# Images optionnelles pour les sections Projets, Blog, Services (Accueil et pages)
	projects_home_image = models.ImageField(upload_to="section_images/", blank=True, null=True, verbose_name=_("Image section Projets (Accueil)"))
	projects_page_image = models.ImageField(upload_to="section_images/", blank=True, null=True, verbose_name=_("Image page liste Projets"))
	blog_home_image = models.ImageField(upload_to="section_images/", blank=True, null=True, verbose_name=_("Image section Blog (Accueil)"))
	blog_page_image = models.ImageField(upload_to="section_images/", blank=True, null=True, verbose_name=_("Image page liste Blog"))
	services_home_image = models.ImageField(upload_to="section_images/", blank=True, null=True, verbose_name=_("Image section Services (Accueil)"))
	services_page_image = models.ImageField(upload_to="section_images/", blank=True, null=True, verbose_name=_("Image page liste Services"))

	# Ordre d'affichage des sections (navbar + page d'accueil)
	projects_display_order = models.PositiveIntegerField(default=2, verbose_name=_("Ordre d'affichage Projets"))
	blog_display_order = models.PositiveIntegerField(default=3, verbose_name=_("Ordre d'affichage Blog"))
	services_display_order = models.PositiveIntegerField(default=4, verbose_name=_("Ordre d'affichage Services"))
	contact_display_order = models.PositiveIntegerField(default=5, verbose_name=_("Ordre d'affichage Contact"))

	# Section Contact - Configuration
	contact_title = models.CharField(max_length=200, blank=True, verbose_name=_("Titre de la section Contact"))
	contact_title_image = models.ImageField(upload_to='section_images/', blank=True, null=True, verbose_name=_("Image du titre Contact"))
	contact_intro_text = RichTextUploadingField(blank=True, verbose_name=_("Texte d'introduction Contact"))
	contact_name_label = models.CharField(max_length=100, default="Nom complet", verbose_name=_("Label champ Nom"))
	contact_email_label = models.CharField(max_length=100, default="Adresse email", verbose_name=_("Label champ Email"))
	contact_company_label = models.CharField(max_length=100, default="Entreprise", verbose_name=_("Label champ Entreprise"))
	contact_profession_label = models.CharField(max_length=100, default="Profession", verbose_name=_("Label champ Profession"))
	contact_subject_label = models.CharField(max_length=100, default="Objet", verbose_name=_("Label champ Objet"))
	contact_message_label = models.CharField(max_length=100, default="Votre message", verbose_name=_("Label champ Message"))
	contact_button_text = models.CharField(max_length=100, default="Envoyer le message", verbose_name=_("Texte du bouton"))
	contact_success_message = models.TextField(default="Merci ! Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.", verbose_name=_("Message de succès"))
	contact_error_message = models.TextField(default="Une erreur s'est produite lors de l'envoi de votre message. Veuillez réessayer.", verbose_name=_("Message d'erreur"))
	enable_confirmation_email = models.BooleanField(default=True, verbose_name=_("Envoyer un email de confirmation à l'expéditeur"))
	gmail_app_password = models.CharField(max_length=100, blank=True, verbose_name=_("Mot de passe d'application Gmail"), help_text=_("Requis pour envoyer des emails. Créez-le sur https://myaccount.google.com/apppasswords"))

	# Configuration Projets - Affichage des métadonnées
	projects_show_author_home = models.BooleanField(default=True, verbose_name=_("Auteur"))
	projects_show_author_list = models.BooleanField(default=True, verbose_name=_("Auteur"))
	projects_show_author_detail = models.BooleanField(default=True, verbose_name=_("Auteur"))
	projects_show_profession_home = models.BooleanField(default=True, verbose_name=_("Profession"))
	projects_show_profession_list = models.BooleanField(default=True, verbose_name=_("Profession"))
	projects_show_profession_detail = models.BooleanField(default=True, verbose_name=_("Profession"))
	projects_show_publish_date_home = models.BooleanField(default=True, verbose_name=_("Date pub"))
	projects_show_publish_date_list = models.BooleanField(default=True, verbose_name=_("Date pub"))
	projects_show_publish_date_detail = models.BooleanField(default=True, verbose_name=_("Date pub"))
	projects_show_update_date_home = models.BooleanField(default=True, verbose_name=_("Date MAJ"))
	projects_show_update_date_list = models.BooleanField(default=True, verbose_name=_("Date MAJ"))
	projects_show_update_date_detail = models.BooleanField(default=True, verbose_name=_("Date MAJ"))
	
	# Configuration Blog - Affichage des métadonnées
	blog_show_author_home = models.BooleanField(default=True, verbose_name=_("Auteur"))
	blog_show_author_list = models.BooleanField(default=True, verbose_name=_("Auteur"))
	blog_show_author_detail = models.BooleanField(default=True, verbose_name=_("Auteur"))
	blog_show_profession_home = models.BooleanField(default=True, verbose_name=_("Profession"))
	blog_show_profession_list = models.BooleanField(default=True, verbose_name=_("Profession"))
	blog_show_profession_detail = models.BooleanField(default=True, verbose_name=_("Profession"))
	blog_show_publish_date_home = models.BooleanField(default=True, verbose_name=_("Date pub"))
	blog_show_publish_date_list = models.BooleanField(default=True, verbose_name=_("Date pub"))
	blog_show_publish_date_detail = models.BooleanField(default=True, verbose_name=_("Date pub"))
	blog_show_update_date_home = models.BooleanField(default=True, verbose_name=_("Date MAJ"))
	blog_show_update_date_list = models.BooleanField(default=True, verbose_name=_("Date MAJ"))
	blog_show_update_date_detail = models.BooleanField(default=True, verbose_name=_("Date MAJ"))
	
	# Configuration Services - Affichage des métadonnées
	services_show_author_home = models.BooleanField(default=True, verbose_name=_("Auteur"))
	services_show_author_list = models.BooleanField(default=True, verbose_name=_("Auteur"))
	services_show_author_detail = models.BooleanField(default=True, verbose_name=_("Auteur"))
	services_show_profession_home = models.BooleanField(default=True, verbose_name=_("Profession"))
	services_show_profession_list = models.BooleanField(default=True, verbose_name=_("Profession"))
	services_show_profession_detail = models.BooleanField(default=True, verbose_name=_("Profession"))
	services_show_publish_date_home = models.BooleanField(default=True, verbose_name=_("Date pub"))
	services_show_publish_date_list = models.BooleanField(default=True, verbose_name=_("Date pub"))
	services_show_publish_date_detail = models.BooleanField(default=True, verbose_name=_("Date pub"))
	services_show_update_date_home = models.BooleanField(default=True, verbose_name=_("Date MAJ"))
	services_show_update_date_list = models.BooleanField(default=True, verbose_name=_("Date MAJ"))
	services_show_update_date_detail = models.BooleanField(default=True, verbose_name=_("Date MAJ"))

	# Relations Many-to-Many pour choisir les contenus à publier par profil
	# Importation dynamique pour éviter les imports circulaires
	published_projects = models.ManyToManyField('app_projet.Project', blank=True, related_name='profiles', verbose_name=_("Projets publiés"))
	featured_projects = models.ManyToManyField('app_projet.Project', blank=True, related_name='featured_in_profiles', verbose_name=_("Projets mis en avant"))
	published_articles = models.ManyToManyField('app_blog.BlogPost', blank=True, related_name='profiles', verbose_name=_("Articles publiés"))
	featured_articles = models.ManyToManyField('app_blog.BlogPost', blank=True, related_name='featured_in_profiles', verbose_name=_("Articles mis en avant"))
	published_services = models.ManyToManyField('app_service.Service', blank=True, related_name='profiles', verbose_name=_("Services publiés"))
	featured_services = models.ManyToManyField('app_service.Service', blank=True, related_name='featured_in_profiles', verbose_name=_("Services mis en avant"))

	# Navigation et layout
	navbar_position = models.CharField(
		max_length=10,
		choices=[('left', 'Gauche'), ('right', 'Droite')],
		default='left',
		verbose_name=_("Position de la barre de navigation"),
		help_text=_("Choisir si la barre de navigation doit être à gauche ou à droite")
	)

	class Meta:
		verbose_name = _("Profil du site")
		verbose_name_plural = _("Profils du site")

	def __str__(self) -> str:
		default_marker = "⭐ " if self.is_default else ""
		published_marker = "📢 " if self.is_published else "🔒 "
		return f"{published_marker}{default_marker}{self.first_name} {self.last_name}" if (self.first_name or self.last_name) else f"{published_marker}{default_marker}SiteProfile"
	
	def get_absolute_url(self):
		"""URL du profil"""
		if self.is_default:
			return "/"
		# Créer l'URL avec paramètres nom et profession AVANT le chemin
		from django.utils.text import slugify
		nom_slug = slugify(f"{self.first_name}-{self.last_name}")
		profession_slug = slugify(self.profession) if self.profession else "profil"
		return f"/profil/nom={nom_slug}&profession={profession_slug}/"
	
	def save(self, *args, **kwargs):
		# Génération automatique du slug à chaque sauvegarde
		from django.utils.text import slugify
		base_slug = slugify(f"{self.first_name or 'prenom'}-{self.last_name or 'nom'}-{self.profession or 'profil'}")
		
		# Vérifier l'unicité du slug et ajouter un numéro si nécessaire
		slug = base_slug
		counter = 1
		while SiteProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
			slug = f"{base_slug}-{counter}"
			counter += 1
		self.slug = slug
		
		# Si ce profil est défini comme défaut, retirer le défaut des autres
		if self.is_default:
			SiteProfile.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
		super().save(*args, **kwargs)

	def get_ordered_sections(self):
		"""Retourne les sections principales dans l'ordre configuré (pour navbar et page d'accueil)"""
		sections = [
			{'type': 'projects', 'order': self.projects_display_order, 'in_navbar': True},
			{'type': 'blog', 'order': self.blog_display_order, 'in_navbar': True},
			{'type': 'services', 'order': self.services_display_order, 'in_navbar': True},
			{'type': 'contact', 'order': self.contact_display_order, 'in_navbar': False},
		]
		return sorted(sections, key=lambda x: x['order'])

	@property
	def initials(self):
		parts = []
		if self.first_name:
			parts.append(self.first_name[0].upper())
		if self.last_name:
			parts.append(self.last_name[0].upper())
		return "".join(parts) or "U"


class Education(models.Model):
	profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="educations")
	title = models.CharField(max_length=255, verbose_name=_("Titre de la formation"))
	date = models.CharField(max_length=100, blank=True, verbose_name=_("Date / Années"))
	institution = models.CharField(max_length=255, blank=True, verbose_name=_("Établissement"))
	icon = models.ImageField(upload_to="education/", blank=True, null=True, verbose_name=_("Icône"))
	# Détails optionnels remplissables depuis l'admin. Si vide, l'icône œil n'est pas affichée.
	details = RichTextUploadingField(blank=True, null=True, verbose_name=_("Détails de la formation"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Formation")
		verbose_name_plural = _("Formations")

	def __str__(self) -> str:
		return f"{self.title} — {self.institution}"


class Experience(models.Model):
	profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="experiences")
	title = models.CharField(max_length=255, verbose_name=_("Intitulé / Poste"))
	date = models.CharField(max_length=100, blank=True, verbose_name=_("Date / Période"))
	company = models.CharField(max_length=255, blank=True, verbose_name=_("Entreprise"))
	company_url = models.URLField(blank=True, verbose_name=_("Lien entreprise"))
	icon = models.ImageField(upload_to="experience/", blank=True, null=True, verbose_name=_("Icône"))
	# Détails optionnels pour une expérience ; affichés via l'icône œil
	details = RichTextUploadingField(blank=True, null=True, verbose_name=_("Détails de l'expérience"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Expérience")
		verbose_name_plural = _("Expériences")

	def __str__(self) -> str:
		return f"{self.title} — {self.company}"


class Section(models.Model):
	"""Section dynamique (Compétences, Stack techniques, Intérêts, Valeurs, Formation, Expérience, etc.)"""
	SECTION_TYPES = (
		('formation', 'Formation'),
		('experience', 'Expérience'),
		('competences', 'Compétences'),
		('stack', 'Stack techniques'),
		('interets', 'Intérêts'),
		('valeurs', 'Valeurs'),
		('custom', 'Personnalisé'),
	)
	
	profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="sections")
	section_type = models.CharField(max_length=20, choices=SECTION_TYPES, verbose_name=_("Type de section"))
	title = models.CharField(max_length=200, verbose_name=_("Titre de la section"))
	title_image = models.ImageField(upload_to="section_images/", blank=True, null=True, verbose_name=_("Image du titre"))
	is_active = models.BooleanField(default=True, verbose_name=_("Afficher cette section"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre d'affichage"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Section")
		verbose_name_plural = _("Sections")

	def __str__(self) -> str:
		return f"{self.title}"


class SectionItem(models.Model):
	"""Item d'une section (compétence, stack, intérêt, valeur, formation, expérience, etc.)"""
	section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="items")
	icon = models.ImageField(upload_to="sections/", blank=True, null=True, verbose_name=_("Icône"))
	title = models.CharField(max_length=255, verbose_name=_("Titre principal"))
	subtitle = models.CharField(max_length=500, blank=True, verbose_name=_("Sous-titre / Détails (ex: institution, entreprise)"))
	date = models.CharField(max_length=100, blank=True, verbose_name=_("Date / Période (ex: 2023, 2022-2023)"))
	url = models.URLField(blank=True, verbose_name=_("Lien (optionnel, ex: site de l'entreprise)"))
	# Détails riches optionnels, similaires à Formation/Expérience
	details = RichTextUploadingField(blank=True, null=True, verbose_name=_("Détails"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Élément de section")
		verbose_name_plural = _("Éléments de section")

	def __str__(self) -> str:
		return f"{self.section.title} - {self.title}"


