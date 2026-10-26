from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Sum, F,Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import RegisterForm, ReviewForm
from .models import CartItem, Categeory, Favorite, Member, Product, ProductImage, Review, Wishlist


DEFAULT_CATEGORIES = [
    "Noutbuklar",
    "Smartfonlar",
    "Kompyuter aksessuarlari",
    "Maishiy texnika",
    "Elektronika",
]


def index(request):
    categories = Categeory.objects.all()
    featured = Product.objects.filter(is_active=True, quantity__gt=0).select_related("category")[:8]
    return render(request, "index.html", {
        "categories": categories,
        "featured": featured,
    })


def products(request):
    product_list = Product.objects.filter(is_active=True).select_related("category")
    categories = Categeory.objects.all()
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    if query:
        product_list = product_list.filter(
            Q(description__icontains=query) | Q(category__nomi__icontains=query)
        )
    if category_slug:
        product_list = product_list.filter(category__slug=category_slug)

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
        )

    return render(request, "product.html", {
        "mahsulot": product_list,
        "categories": categories,
        "query": query,
        "selected_category": category_slug,
        "favorite_ids": favorite_ids,
    })


def product_view(request, slug):
    mahsulot = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("images", "likes"),
        slug=slug, is_active=True
    )
    reviews = mahsulot.reviews.select_related("user").order_by("-created_at")
    average_rating = reviews.aggregate(avg=Avg("rating"))["avg"]
    average_rating = round(average_rating, 1) if average_rating is not None else 0

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Sharh qoldirish uchun tizimga kiring.")
            return redirect(f"{reverse('login')}?next={request.path}")
        form = ReviewForm(request.POST)
        if form.is_valid():
            if Review.objects.filter(product=mahsulot, user=request.user).exists():
                messages.warning(request, "Siz bu mahsulotga avval sharh qoldirgansiz.")
            else:
                review = form.save(commit=False)
                review.product = mahsulot
                review.user = request.user
                review.save()
                messages.success(request, "Sharhingiz muvaffaqiyatli yuborildi!")
            return redirect("product-view", slug=mahsulot.slug)
    else:
        form = ReviewForm()

    Product.objects.filter(pk=mahsulot.pk).update(views_count=F("views_count") + 1)
    mahsulot.refresh_from_db(fields=["views_count"])
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(
        user=request.user, product=mahsulot
    ).exists()
    liked = request.user.is_authenticated and mahsulot.likes.filter(
        pk=request.user.pk
    ).exists()
    related = Product.objects.filter(
        category=mahsulot.category, is_active=True
    ).exclude(pk=mahsulot.pk)[:4]
    gallery_images = list(mahsulot.images.all())

    return render(request, "product_detail.html", {
        "mahsulot": mahsulot,
        "is_favorite": is_favorite,
        "related": related,
        "liked": liked,
        "like_count": mahsulot.likes.count(),
        "views_count": mahsulot.views_count,
        "gallery_images": gallery_images,
        "reviews": reviews,
        "form": form,
        "average_rating": average_rating,
        "review_count": reviews.count(),
    })


def login_form(request):
    if request.user.is_authenticated:
        return redirect("products")

    next_url = request.GET.get("next") or request.POST.get("next") or ""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Muvaffaqiyatli kirdingiz! 👋")
            return redirect(next_url or "index")

        messages.error(request, "Username yoki parol noto'g'ri.")

    return render(request, "login.html", {"next": next_url})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("products")

    next_url = request.GET.get("next") or request.POST.get("next") or ""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            messages.success(request, "Akkauntingiz yaratildi. Endi tizimga kiring! ✨")
            url = reverse("login")
            if next_url:
                url += f"?next={next_url}"
            return redirect(url)
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form, "next": next_url})


def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect("index")


@login_required(login_url="login")
def cart(request):
    items = CartItem.objects.filter(user=request.user).select_related("product", "product__category")
    favorites = Favorite.objects.filter(user=request.user).select_related("product", "product__category")
    total = sum((item.subtotal for item in items), Decimal("0.00"))
    count = sum(item.quantity for item in items)
    return render(request, "cart.html", {
        "cart_items": items,
        "favorites": favorites,
        "cart_total": total,
        "cart_count": count,
    })


@login_required(login_url="login")
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("products")
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if product.quantity < 1:
        messages.error(request, "Bu mahsulot hozircha tugagan.")
        return redirect(request.POST.get("next") or "products")

    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if created:
        item.quantity = 1
    else:
        item.quantity = min(item.quantity + 1, product.quantity, 100)
    item.save()
    messages.success(request, f"{product.description} savatga qo'shildi. 🛒")
    return redirect(request.POST.get("next") or "products")


@login_required(login_url="login")
def update_cart(request, item_id):
    if request.method != "POST":
        return redirect("cart")
    item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    try:
        quantity = int(request.POST.get("quantity", item.quantity))
    except (TypeError, ValueError):
        quantity = item.quantity

    quantity = max(1, min(quantity, item.product.quantity, 100))
    item.quantity = quantity
    item.save()
    return redirect("cart")


@login_required(login_url="login")
def remove_from_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(CartItem, pk=item_id, user=request.user)
        item.delete()
        messages.success(request, "Mahsulot savatdan olib tashlandi.")
    return redirect("cart")


@login_required(login_url="login")
def toggle_favorite(request, product_id):
    if request.method != "POST":
        return redirect("products")
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
        messages.success(request, "Sevimlilardan olib tashlandi.")
    else:
        messages.success(request, "Sevimlilarga qo'shildi. ❤️")
    return redirect(request.POST.get("next") or "products")


@login_required(login_url="login")
@require_POST
def like_view(request, slug):
    mahsulot = get_object_or_404(Product, slug=slug, is_active=True)
    if mahsulot.likes.filter(pk=request.user.pk).exists():
        mahsulot.likes.remove(request.user)
    else:
        mahsulot.likes.add(request.user)
    return redirect(request.POST.get("next") or request.META.get("HTTP_REFERER") or "product-view")


@login_required(login_url="login")
def wishlist_list(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    context = {
        'wishlist_items' : wishlist_items
    }
    return render(request, 'wishlist.html',context)



def appearance_settings(request):
    """Foydalanuvchining brauzerda saqlanadigan ko'rinish sozlamalari sahifasi."""
    return render(request, "appearance_settings.html")
