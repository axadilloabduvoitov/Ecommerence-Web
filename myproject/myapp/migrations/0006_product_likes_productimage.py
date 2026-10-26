# Generated for NovaStore product likes and image gallery.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0005_alter_categeory_options_alter_product_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="likes",
            field=models.ManyToManyField(blank=True, related_name="liked_products", to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="products/gallery/")),
                ("alt_text", models.CharField(blank=True, max_length=255)),
                ("ordering", models.PositiveIntegerField(default=0)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="myapp.product")),
            ],
            options={
                "ordering": ["ordering", "id"],
                "verbose_name": "Mahsulot rasmi",
                "verbose_name_plural": "Mahsulot rasmlari",
            },
        ),
    ]
