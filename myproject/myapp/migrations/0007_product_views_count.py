from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0006_product_likes_productimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="views_count",
            field=models.PositiveBigIntegerField(default=0, verbose_name="Ko'rishlar soni"),
        ),
    ]
