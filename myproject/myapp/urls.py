from django.urls import path
from . import views

urlpatterns = [
    path("appearance/", views.appearance_settings, name="appearance-settings"),
    path("", views.index, name="index"),
    path("products/", views.products, name="products"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add-to-cart"),
    path("cart/update/<int:item_id>/", views.update_cart, name="update-cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove-from-cart"),
    path("favorite/toggle/<int:product_id>/", views.toggle_favorite, name="toggle-favorite"),
    path("login/", views.login_form, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("product/<slug:slug>/", views.product_view, name="product-view"),
    path("likes/<slug:slug>/", views.like_view, name="like-view"),
]

