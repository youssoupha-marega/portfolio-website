"""
Tests unitaires pour verifier l'affichage des metadonnees de services dans l'accueil.
"""

from datetime import datetime

from django.template.loader import get_template
from django.test import Client, TestCase

from app_acceuil.models import SiteProfile
from app_service.models import Service


class ServiceMetadataTest(TestCase):
    def setUp(self):
        self.profile = SiteProfile.objects.create(
            first_name="Test",
            last_name="User",
            profession="Developer",
            email="test@example.com",
            is_default=True,
            is_published=True,
            services_show_author_home=True,
            services_show_profession_home=True,
            services_show_publish_date_home=True,
            services_show_update_date_home=True,
        )

        self.service = Service.objects.create(
            title="Service Test",
            slug="service-test",
            resume="Resume du service test",
            content="Contenu du service test",
            author_name="Youssoupha Marega",
            author_profession="Data Scientist",
            author_email="youssoupha@example.com",
            published_at=datetime(2025, 12, 6),
            updated_at=datetime(2025, 12, 8),
        )

        self.service.is_published = True
        self.service.save()

        self.profile.published_services.add(self.service)
        self.profile.featured_services.add(self.service)

        self.client = Client()

    def test_service_has_metadata(self):
        self.assertEqual(self.service.author_name, "Youssoupha Marega")
        self.assertEqual(self.service.author_profession, "Data Scientist")
        self.assertIsNotNone(self.service.published_at)
        self.assertIsNotNone(self.service.updated_at)

    def test_profile_metadata_settings(self):
        self.assertTrue(self.profile.services_show_author_home)
        self.assertTrue(self.profile.services_show_profession_home)
        self.assertTrue(self.profile.services_show_publish_date_home)
        self.assertTrue(self.profile.services_show_update_date_home)

    def test_home_page_context(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("site_profile", response.context)
        self.assertIn("services", response.context)
        self.assertGreaterEqual(len(response.context["services"]), 1)

    def test_home_page_renders_metadata(self):
        response = self.client.get("/")
        content = response.content.decode("utf-8")

        self.assertIn("Youssoupha Marega", content)

    def test_debug_template_variables(self):
        context = {
            "site_profile": self.profile,
            "services": [self.service],
        }

        template = get_template("includes/section_services.html")
        html = template.render(context)

        self.assertIn("Youssoupha Marega", html)
        self.assertIn("Data Scientist", html)
