from django.contrib import admin
from .models import Member, Product, ProductImage, Categeory, CartItem, Favorite


@admin.register(Categeory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "nomi", "slug", "product_count")
    search_fields = ("nomi",)
    prepopulated_fields = {"slug": ("nomi",)}

    @admin.display(description="Mahsulotlar")
    def product_count(self, obj):
        return obj.products.count()


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ("id", "description", "category", "price", "quantity", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("description",)
    list_editable = ("price", "quantity", "is_active")
    prepopulated_fields = {"slug": ("description",)}
    ordering = ("-id",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "ism", "familya", "yosh", "email")
    search_fields = ("ism", "familya", "email")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "subtotal")
    search_fields = ("user__username", "product__description")
    list_filter = ("product__category",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    search_fields = ("user__username", "product__description")
    list_filter = ("product__category",)
