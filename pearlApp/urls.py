from django.urls import path
from . import views

urlpatterns = [
    # General URLs
    path("", views.landing, name="landing"),
    path("home/", views.home, name="home"),
    path("terms/", views.terms_view, name="terms"),
    path("contact/", views.contact_view, name="contact"),
    path("faqs/", views.faqs_view, name="faqs"),
    path("about/", views.about_view, name="about"),

    # Authentication URLs
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("password_reset/", views.reset_password_view,
         name="password_reset"),


    path("orders/", views.orders_view, name="orders"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("cart/", views.cart_view, name="cart"),

    # Store URLs
    path("store/gas/", views.gas_view, name="gas"),
    path("store/aquarium/", views.aquarium_view, name="aquarium"),
    path("store/supplements/", views.supplements_view, name="supplements"),
    path("store/electronics/", views.electronics_view, name="electronics"),
]
