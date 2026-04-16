from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_acceuil", "0040_alter_education_details_alter_experience_details_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteprofile",
            name="services_page_enabled",
            field=models.BooleanField(
                default=True,
                verbose_name="Pages liste et détail des services actives",
                help_text=(
                    "Décocher pour désactiver les pages /services/ et /services/<slug>/. "
                    "Le lien 'Services' dans la navbar et les boutons 'En savoir plus' renverront "
                    "vers la section #services de la page d'accueil."
                ),
            ),
        ),
    ]
