from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Categeory(models.Model):
    nomi = models.CharField("Nomi", max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["nomi"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nomi)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nomi


class Member(models.Model):
    ism = models.CharField("Ism", max_length=20)
    familya = models.CharField("Familya", max_length=25)
    yosh = models.IntegerField(null=True, blank=True)
    email = models.EmailField("Email")

    def __str__(self):
        return f"{self.ism} {self.familya}"


class Product(models.Model):
    category = models.ForeignKey(
        Categeory,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Kategoriya",
    )

    image = models.ImageField(upload_to="products/", blank=True, null=True)
    description = models.CharField("Mahsulot nomi", max_length=255)
    price = models.DecimalField("Narxi (so'm)", max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal("0.01"))])
    quantity = models.PositiveIntegerField("Ombordagi soni", default=0)
    is_active = models.BooleanField("Faol", default=True)
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_products", blank=True)
    views_count = models.PositiveBigIntegerField("Ko'rishlar soni", default=0)

    def like_soni(self):
        return self.likes.count()

    class Meta:
        ordering = ["-id"]
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def save(self, *args, **kwargs):
        base = slugify(self.description) or "product"
        slug = base
        counter = 2
        while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{counter}"
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description


class CartItem(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)

    korishlar = models.PositiveBigIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="likes_products",blank=True)

    def like_soni(self):
        return self.likes.count()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_user_product_cart")
        ]

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user.username} — {self.product.description} x{self.quantity}"


class Favorite(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_user_product_favorite")
        ]

    def __str__(self):
        return f"{self.user.username} ♥ {self.product.description}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=255, blank=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordering", "id"]
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"

    def __str__(self):
        return f"{self.product.description} — rasm {self.pk}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f"{i} Yulduz") for i in range(1, 6)], default=5, verbose_name="Reyting")
    comment = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    def __str__(self):
        return f"{self.user.username} - {self.product.description} ({self.rating})⭐️"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'products')