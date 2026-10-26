from decimal import Decimal
from django.db import migrations, models
from django.core.validators import MinValueValidator


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0003_store_upgrade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=12,
                validators=[MinValueValidator(Decimal("0.01"))],
                verbose_name="Narxi (so'm)",
            ),
        ),
    ]
