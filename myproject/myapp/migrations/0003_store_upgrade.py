from django.db import migrations, models
import django.db.models.deletion
import django.utils.text


DEFAULT_CATEGORIES = [
    "Noutbuklar",
    "Smartfonlar",
    "Kompyuter aksessuarlari",
    "Maishiy texnika",
    "Elektronika",
]


def seed_categories_and_clear_products(apps, schema_editor):
    Category = apps.get_model("myapp", "Categeory")
    Product = apps.get_model("myapp", "Product")
    Product.objects.all().delete()
    for name in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(
            nomi=name,
            defaults={"slug": django.utils.text.slugify(name)},
        )


def reverse_seed(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_remove_product_category_product_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="categeory",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="products",
                to="myapp.categeory",
                verbose_name="Kategoriya",
            ),
        ),
        migrations.AlterField(
            model_name="categeory",
            name="nomi",
            field=models.CharField(max_length=100, unique=True, verbose_name="Nomi"),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.CharField(max_length=255, verbose_name="Mahsulot nomi"),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Narxi (so'm)"),
        ),
        migrations.AlterField(
            model_name="product",
            name="quantity",
            field=models.PositiveIntegerField(default=0, verbose_name="Ombordagi soni"),
        ),
        migrations.AlterField(
            model_name="product",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Faol"),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cart_items", to="myapp.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cart_items", to="auth.user")),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(fields=("user", "product"), name="unique_user_product_cart")
                ],
            },
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorited_by", to="myapp.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to="auth.user")),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(fields=("user", "product"), name="unique_user_product_favorite")
                ],
            },
        ),
        migrations.RunPython(seed_categories_and_clear_products, reverse_seed),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="products",
                to="myapp.categeory",
                verbose_name="Kategoriya",
            ),
        ),
    ]
