# pearlApp/views.py
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Category, Product, Cart
from .forms import ProfileUpdateForm

User = get_user_model()


# ----------------- helper -----------------
def _get_cart_count(user):
    """Return number of cart rows for the user (0 if anonymous)."""
    if user.is_authenticated:
        return Cart.objects.filter(user=user).count()
    return 0


# ================== Home Page ==================
def home(request):
    """A simple home view (keeps existing name)."""
    return render(request, "generic/home.html")


def landing_view(request):
    """Landing page: categories, featured and latest products."""
    categories = Category.objects.all()

    # Featured: those with discount first; otherwise latest
    featured = Product.objects.filter(
        discount__gt=0).order_by("-created_at")[:8]
    if not featured:
        featured = Product.objects.all().order_by("-created_at")[:8]

    # Latest products (limit)
    products = Product.objects.all().order_by("-created_at")[:20]

    context = {
        "categories": categories,
        "products": products,
        "featured_products": featured,
        "cart_count": _get_cart_count(request.user),
    }
    return render(request, "generic/landing.html", context)


# ---------------- Category pages ----------------
def category_view(request, slug):
    """Single category page — keeps the function & template name as requested."""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category=category).order_by("-created_at")

    # simple pagination: 12 per page (optional)
    paginator = Paginator(products, 12)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    context = {
        "category": category,
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "cart_count": _get_cart_count(request.user),
    }
    return render(request, "stores/category_products.html", context)


def category_products_view(request, slug):
    """Alternate category view (keeps the function name + template you used)."""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category=category).order_by("-created_at")

    paginator = Paginator(products, 12)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    context = {
        "category": category,
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "cart_count": _get_cart_count(request.user),
    }
    return render(request, "stores/category_products.html", context)


# ================== Product Detail Page ==================
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product,
        "cart_count": _get_cart_count(request.user),
    }
    return render(request, "stores/product_detail.html", context)


# ================= Authentication Views =================
def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not email or not contact or not password1:
            messages.error(request, "Please fill all required fields.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Use custom manager to create user
        try:
            user = User.objects.create_user(
                email=email, contact=contact, password=password1)
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect("signup")

        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("home")

    return render(request, "auth/signup.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # redirect to landing/home as your app expects
            return redirect("landing")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            contact = form.cleaned_data.get("contact")
            password = form.cleaned_data.get("password1")

            user.contact = contact
            if password:
                user.set_password(password)
            user.save()

            messages.success(request, "Profile updated successfully!")
            # If password changed, re-auth might be required in real app
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "auth/profile.html", {"form": form, "cart_count": _get_cart_count(request.user)})


def reset_password_view(request):
    return render(request, "auth/reset_password.html")


# ================= Static/Generic pages =================
def orders_view(request):
    return render(request, "stores/orders.html")


def terms_view(request):
    return render(request, "generic/terms.html")


def contact_view(request):
    return render(request, "generic/contact.html")


def faqs_view(request):
    return render(request, "generic/faqs.html")


def about_view(request):
    return render(request, "generic/about.html")


# ================= Search =================
def search(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(
            category__name__icontains=query)
    ).order_by("-created_at") if query else Product.objects.none()

    return render(request, "generic/search_results.html", {"products": products, "query": query, "cart_count": _get_cart_count(request.user)})


# ================= Store simple pages (render templates) =================
def gas_view(request):
    # Fetch gas category if exists and its products for dynamic rendering
    try:
        cat = Category.objects.get(slug="gas")
        products = Product.objects.filter(category=cat).order_by("-created_at")
    except Category.DoesNotExist:
        products = Product.objects.none()

    return render(request, "stores/gas.html", {"products": products, "cart_count": _get_cart_count(request.user)})


def aquarium_view(request):
    try:
        cat = Category.objects.get(slug="aquarium")
        products = Product.objects.filter(category=cat).order_by("-created_at")
    except Category.DoesNotExist:
        products = Product.objects.none()

    return render(request, "stores/aquarium.html", {"products": products, "cart_count": _get_cart_count(request.user)})


def supplements_view(request):
    try:
        cat = Category.objects.get(slug="supplements")
        products = Product.objects.filter(category=cat).order_by("-created_at")
    except Category.DoesNotExist:
        products = Product.objects.none()

    return render(request, "stores/supplements.html", {"products": products, "cart_count": _get_cart_count(request.user)})


def electronics_view(request):
    try:
        cat = Category.objects.get(slug="electronics")
        products = Product.objects.filter(category=cat).order_by("-created_at")
    except Category.DoesNotExist:
        products = Product.objects.none()

    return render(request, "stores/electronics.html", {"products": products, "cart_count": _get_cart_count(request.user)})


# ================= Cart (using existing Cart model where each row = a product for a user) =================
@login_required
def add_to_cart(request, product_id):
    """
    Adds the product to the user's cart (one Cart row per product + user).
    URL: cart/add/<int:product_id>/
    """
    product = get_object_or_404(Product, pk=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    # If request came from product_detail, go back there; otherwise to cart page
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("cart")


@login_required
def cart_view(request):
    """
    Show cart rows (Cart model) for the logged-in user.
    """
    cart_items = Cart.objects.filter(
        user=request.user).select_related("product")
    total = sum(item.subtotal() for item in cart_items)

    return render(request, "stores/cart.html", {"cart_items": cart_items, "total": total, "cart_count": _get_cart_count(request.user)})


@login_required
def update_cart(request, pk):
    """
    Update quantity for a Cart row. URL: cart/update/<int:pk>/
    """
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)

    # Accept POST form with 'quantity'
    if request.method == "POST":
        try:
            qty = int(request.POST.get("quantity", cart_item.quantity))
        except (TypeError, ValueError):
            qty = cart_item.quantity

        if qty <= 0:
            cart_item.delete()
            messages.info(request, "Item removed from cart.")
        else:
            cart_item.quantity = qty
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
    return redirect("cart")


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from your cart.")
    return redirect("cart")


# ================= Wishlist (session-backed simple implementation) =================
@login_required
def add_to_wishlist(request, product_id):
    """
    Simple session-based wishlist so we don't need a DB model.
    If the user is logged in, we still store wishlist ids in session.
    """
    product = get_object_or_404(Product, pk=product_id)
    wishlist = request.session.get("wishlist", [])

    if product_id in wishlist:
        wishlist.remove(product_id)
        messages.info(request, f"{product.name} removed from wishlist.")
    else:
        wishlist.append(product_id)
        messages.success(request, f"{product.name} added to wishlist.")

    request.session["wishlist"] = wishlist
    # return to referer or wishlist page
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("wishlist")


def wishlist_view(request):
    """
    Display products saved in session wishlist (or empty).
    """
    ids = request.session.get("wishlist", [])
    products = Product.objects.filter(id__in=ids)
    return render(request, "stores/wishlist.html", {"products": products, "cart_count": _get_cart_count(request.user)})
