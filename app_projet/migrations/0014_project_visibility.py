from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_projet", "0013_alter_project_content_alter_project_demo_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="afficher_liste",
            field=models.BooleanField(default=True, verbose_name="Afficher dans la liste"),
        ),
        migrations.AddField(
            model_name="project",
            name="afficher_detail",
            field=models.BooleanField(default=True, verbose_name="Afficher la page de détail"),
        ),
    ]
