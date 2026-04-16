from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_service", "0009_alter_service_statut"),
    ]

    operations = [
        # Champs de visibilité
        migrations.AddField(
            model_name="service",
            name="afficher_liste",
            field=models.BooleanField(default=True, verbose_name="Afficher dans la liste"),
        ),
        migrations.AddField(
            model_name="service",
            name="afficher_detail",
            field=models.BooleanField(default=True, verbose_name="Afficher la page de détail"),
        ),
        # Champs spécifiques aux services
        migrations.AddField(
            model_name="service",
            name="duree",
            field=models.CharField(blank=True, default="", max_length=100, verbose_name="Durée estimée du projet (ex: '4–8 semaines')"),
        ),
        migrations.AddField(
            model_name="service",
            name="localisation",
            field=models.CharField(blank=True, default="Remote / Montréal", max_length=200, verbose_name="Localisation"),
        ),
        migrations.AddField(
            model_name="service",
            name="livrables_label",
            field=models.CharField(blank=True, default="Livrables", max_length=100, verbose_name="Titre de la section livrables (ex: 'Livrables', 'Modules')"),
        ),
        # Modèle Livrable
        migrations.CreateModel(
            name="Livrable",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("contenu", models.CharField(max_length=500, verbose_name="Contenu")),
                ("ordre", models.PositiveIntegerField(default=0, verbose_name="Ordre")),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="livrables",
                        to="app_service.service",
                        verbose_name="Service",
                    ),
                ),
            ],
            options={
                "verbose_name": "Livrable",
                "verbose_name_plural": "Livrables",
                "ordering": ("ordre", "id"),
            },
        ),
    ]
