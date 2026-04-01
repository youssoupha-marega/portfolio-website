from django.db import migrations, models


def forward_map_statuses(apps, schema_editor):
    BlogPost = apps.get_model("app_blog", "BlogPost")
    mapping = {
        "draft": "planning",
        "in_progress": "in_progress",
        "paused": "paused",
        "published": "deployed",
        "deployed": "deployed",
        "completed": "completed",
        "archived": "archived",
    }
    for old_value, new_value in mapping.items():
        BlogPost.objects.filter(statut=old_value).update(statut=new_value)


def backward_map_statuses(apps, schema_editor):
    BlogPost = apps.get_model("app_blog", "BlogPost")
    mapping = {
        "planning": "draft",
        "in_progress": "in_progress",
        "paused": "paused",
        "deployed": "published",
        "completed": "completed",
        "archived": "archived",
    }
    for old_value, new_value in mapping.items():
        BlogPost.objects.filter(statut=old_value).update(statut=new_value)


class Migration(migrations.Migration):
    dependencies = [
        ("app_blog", "0012_blogpoststackitem"),
    ]

    operations = [
        migrations.RunPython(forward_map_statuses, backward_map_statuses),
        migrations.AlterField(
            model_name="blogpost",
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
