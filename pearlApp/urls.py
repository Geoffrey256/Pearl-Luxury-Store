from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("profile/", views.profile_view, name="profile"),
    path("orders/", views.orders_view, name="orders"),      # placeholder
    path("wishlist/", views.wishlist_view, name="wishlist"),  # placeholder
    path("cart/", views.cart_view, name="cart"),            # placeholder
    path("terms/", views.terms_view, name="terms"),          # placeholder
    path("password_reset/", views.reset_password_view,
         name="password_reset"),  # placeholder
]
