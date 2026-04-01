from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_blog", "0011_blogpost_domaine_blogpost_stack_blogpost_statut_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogPostStackItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Nom")),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog_stack/",
                        verbose_name="Logo",
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Ordre")),
                (
                    "blog_post",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="stack_items",
                        to="app_blog.blogpost",
                        verbose_name="Article de blog",
                    ),
                ),
            ],
            options={
                "verbose_name": "Stack blog",
                "verbose_name_plural": "Stacks blog",
                "ordering": ("order", "id"),
            },
        ),
    ]
