from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_projet", "0011_update_project_status_choices"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="statut",
            field=models.CharField(
                blank=True,
                choices=[
                    ("planning", "En planification"),
                    ("in_progress", "En cours"),
                    ("paused", "En pause"),
                    ("deployed", "Déployé"),
                    ("completed", "Terminé"),
                    ("archived", "Archivé"),
                ],
                default="",
                max_length=20,
                verbose_name="Statut",
            ),
        ),
    ]
