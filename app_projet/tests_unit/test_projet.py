"""
Tests pour l'application app_projet.

Couvre:
- Modèle: Project
- Vues: projet_list, projet_detail, profile_projet_list, profile_projet_detail
- URLs: racine et profil
"""

from django.test import TestCase, Client
from django.urls import reverse
from app_projet.models import Project
from app_acceuil.models import SiteProfile


class ProjectModelTest(TestCase):
    """Tests pour le modèle Project."""
    
    def setUp(self):
        """Créer des projets de test."""
        self.project = Project.objects.create(
            title="Dashboard d'analyse de données",
            resume="Un dashboard interactif pour l'analyse de données",
            content="<p>Contenu détaillé du projet</p>",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst",
            github_url="https://github.com/test/project",
            demo_url="https://demo.example.com"
        )
    
    def test_project_creation(self):
        """Tester la création d'un projet."""
        self.assertEqual(self.project.title, "Dashboard d'analyse de données")
        self.assertEqual(self.project.author_name, "Yama Sakho")
        self.assertEqual(self.project.github_url, "https://github.com/test/project")
    
    def test_project_slug_generation(self):
        """Tester la génération du slug."""
        self.assertEqual(self.project.slug, "dashboard-danalyse-de-donnees")
    
    def test_project_get_absolute_url(self):
        """Tester get_absolute_url."""
        url = self.project.get_absolute_url()
        expected = reverse('projet_detail', kwargs={'slug': self.project.slug})
        self.assertEqual(url, expected)
    
    def test_project_str_method(self):
        """Tester la méthode __str__."""
        self.assertEqual(str(self.project), "Dashboard d'analyse de données")
    
    def test_project_optional_fields(self):
        """Tester les champs optionnels."""
        project = Project.objects.create(
            title="Minimal Project",
            resume="Resume",
            content="Content",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Dev"
        )
        self.assertEqual(project.github_url, "")
        self.assertEqual(project.demo_url, "")
        self.assertIsNone(project.main_image.name)


class ProjectListViewTest(TestCase):
    """Tests pour la vue de liste des projets (racine)."""
    
    def setUp(self):
        """Créer des projets de test."""
        self.client = Client()
        
        self.project1 = Project.objects.create(
            title="Project 1",
            resume="Resume 1",
            content="Content 1",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Dev"
        )
        
        self.project2 = Project.objects.create(
            title="Project 2",
            resume="Resume 2",
            content="Content 2",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Dev"
        )
    
    def test_list_view_status_code(self):
        """Tester que la page de liste se charge."""
        response = self.client.get(reverse('projet_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_list_view_uses_correct_template(self):
        """Tester que la vue utilise le bon template."""
        response = self.client.get(reverse('projet_list'))
        self.assertTemplateUsed(response, 'app_projet/list.html')
    
    def test_list_view_contains_projects(self):
        """Tester que la vue contient les projets."""
        response = self.client.get(reverse('projet_list'))
        self.assertIn('projets', response.context)
        self.assertEqual(len(response.context['projets']), 2)
    
    def test_list_view_projects_ordered_by_date(self):
        """Tester que les projets sont triés par date (plus récent en premier)."""
        response = self.client.get(reverse('projet_list'))
        projets = list(response.context['projets'])
        # Les projets doivent être triés du plus récent au plus ancien
        # Comme project2 a été créé après project1, il devrait être en premier
        self.assertEqual(len(projets), 2)
        self.assertGreaterEqual(projets[0].created_at, projets[1].created_at)

    def test_list_view_renders_github_and_demo_buttons_when_links_exist(self):
        """Tester que les boutons GitHub et Démo apparaissent quand les URLs sont renseignées."""
        project = Project.objects.create(
            title="Project With Links",
            resume="Resume with links",
            content="Content with links",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Dev",
            github_url="https://github.com/test/project-with-links",
            demo_url="https://demo.example.com/project-with-links",
        )

        response = self.client.get(reverse('projet_list'))

        self.assertContains(response, project.title)
        self.assertContains(response, 'href="https://github.com/test/project-with-links"')
        self.assertContains(response, 'href="https://demo.example.com/project-with-links"')


class ProjectDetailViewTest(TestCase):
    """Tests pour la vue de détail d'un projet (racine)."""
    
    def setUp(self):
        """Créer un projet de test."""
        self.client = Client()
        
        self.project = Project.objects.create(
            title="Test Project",
            resume="Test resume",
            content="Test content",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Dev"
        )
    
    def test_detail_view_status_code(self):
        """Tester que la page de détail se charge."""
        response = self.client.get(
            reverse('projet_detail', kwargs={'slug': self.project.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view_uses_correct_template(self):
        """Tester que la vue utilise le bon template."""
        response = self.client.get(
            reverse('projet_detail', kwargs={'slug': self.project.slug})
        )
        self.assertTemplateUsed(response, 'app_projet/detail.html')
    
    def test_detail_view_contains_project(self):
        """Tester que la vue contient le projet."""
        response = self.client.get(
            reverse('projet_detail', kwargs={'slug': self.project.slug})
        )
        self.assertEqual(response.context['projet'].id, self.project.id)
    
    def test_detail_view_404_for_invalid_slug(self):
        """Tester que la vue retourne 404 pour un slug invalide."""
        response = self.client.get(
            reverse('projet_detail', kwargs={'slug': 'slug-inexistant'})
        )
        self.assertEqual(response.status_code, 404)


class ProfileProjectViewsTest(TestCase):
    """Tests pour les vues de projets avec contexte profil."""
    
    def setUp(self):
        """Créer un profil et des projets de test."""
        self.client = Client()
        
        # Créer un profil
        self.profile = SiteProfile.objects.create(
            first_name="Yama",
            last_name="Sakho",
            profession="Data Analyst",
            is_published=True,
            is_default=False
        )
        
        # Créer des projets
        self.project1 = Project.objects.create(
            title="Project 1",
            resume="Resume 1",
            content="Content 1",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst"
        )
        
        self.project2 = Project.objects.create(
            title="Project 2",
            resume="Resume 2",
            content="Content 2",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst"
        )
        
        # Associer les projets au profil
        self.profile.published_projects.add(self.project1, self.project2)
    
    def test_profile_list_view_status_code(self):
        """Tester que la liste profil se charge."""
        response = self.client.get(
            reverse('profile_projet_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertEqual(response.status_code, 200)
    
    def test_profile_list_view_contains_profile_projects(self):
        """Tester que la liste contient les projets du profil."""
        response = self.client.get(
            reverse('profile_projet_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertIn('projets', response.context)
        self.assertEqual(len(response.context['projets']), 2)
    
    def test_profile_list_view_contains_profile_context(self):
        """Tester que le contexte contient le profil."""
        response = self.client.get(
            reverse('profile_projet_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertIn('site_profile', response.context)
        self.assertEqual(response.context['site_profile'].id, self.profile.id)
    
    def test_profile_detail_view_status_code(self):
        """Tester que le détail profil se charge."""
        response = self.client.get(
            reverse('profile_projet_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.project1.slug
            })
        )
        self.assertEqual(response.status_code, 200)
    
    def test_profile_detail_view_contains_project(self):
        """Tester que le détail contient le projet."""
        response = self.client.get(
            reverse('profile_projet_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.project1.slug
            })
        )
        self.assertEqual(response.context['projet'].id, self.project1.id)
    
    def test_profile_detail_404_if_profile_not_found(self):
        """Tester 404 si le profil n'existe pas."""
        response = self.client.get(
            reverse('profile_projet_detail', kwargs={
                'nom': 'invalid-name',
                'profession': 'invalid-profession',
                'slug': self.project1.slug
            })
        )
        self.assertEqual(response.status_code, 404)
    
    def test_profile_detail_404_if_project_not_found(self):
        """Tester 404 si le projet n'existe pas."""
        response = self.client.get(
            reverse('profile_projet_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': 'slug-inexistant'
            })
        )
        self.assertEqual(response.status_code, 404)


class ProjectURLTest(TestCase):
    """Tests pour les URLs des projets."""
    
    def test_root_list_url_resolves(self):
        """Tester que l'URL de liste racine est correcte."""
        url = reverse('projet_list')
        self.assertEqual(url, '/projets/')
    
    def test_root_detail_url_resolves(self):
        """Tester que l'URL de détail racine est correcte."""
        url = reverse('projet_detail', kwargs={'slug': 'test-project'})
        self.assertEqual(url, '/projets/test-project/')
    
    def test_profile_list_url_resolves(self):
        """Tester que l'URL de liste profil est correcte."""
        url = reverse('profile_projet_list', kwargs={
            'nom': 'yama-sakho',
            'profession': 'data-analyst'
        })
        self.assertEqual(url, '/profil/nom=yama-sakho&profession=data-analyst/projets/')
    
    def test_profile_detail_url_resolves(self):
        """Tester que l'URL de détail profil est correcte."""
        url = reverse('profile_projet_detail', kwargs={
            'nom': 'yama-sakho',
            'profession': 'data-analyst',
            'slug': 'test-project'
        })
        self.assertEqual(
            url,
            '/profil/nom=yama-sakho&profession=data-analyst/projets/test-project/'
        )

