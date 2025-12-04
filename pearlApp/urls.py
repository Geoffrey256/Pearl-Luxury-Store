from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # General URLs
    path("", views.landing_view, name="landing"),
    path("home/", views.home, name="home"),
    path("terms/", views.terms_view, name="terms"),
    path("contact/", views.contact_view, name="contact"),
    path("faqs/", views.faqs_view, name="faqs"),
    path("about/", views.about_view, name="about"),
    path('search/', views.search, name='search'),

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
    #     path("add-to-cart/<int:product_id>/",
    #          views.add_to_cart, name="add_to_cart"),
    #     path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:pk>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),

    path('wishlist/add/<int:product_id>/',
         views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/',
         views.remove_from_wishlist, name='remove_from_wishlist'),



    # Store URLs
    path("store/gas/", views.gas_view, name="gas"),
    path("store/aquarium/", views.aquarium_view, name="aquarium"),
    path("store/supplements/", views.supplements_view, name="supplements"),
    path("store/electronics/", views.electronics_view, name="electronics"),
    path("category/<slug:slug>/", views.category_view, name="category"),
    path("product/<int:pk>/", views.product_detail_view, name="product_detail"),
    path("category/<slug:slug>/products/",
         views.category_products_view, name="category_products"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
