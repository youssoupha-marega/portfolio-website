from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_blog", "0015_blogpost_demo_url_blogpost_github_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="afficher_liste",
            field=models.BooleanField(default=True, verbose_name="Afficher dans la liste"),
        ),
        migrations.AddField(
            model_name="blogpost",
            name="afficher_detail",
            field=models.BooleanField(default=True, verbose_name="Afficher la page de détail"),
        ),
    ]
