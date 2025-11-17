from .forms import ProfileUpdateForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    return render(request, "home.html")


def landing(request):
    return render(request, "generic/land.html")


User = get_user_model()


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Use custom manager to create user
        user = User.objects.create_user(
            email=email, contact=contact, password=password1)

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
            return redirect("/")  # or redirect("home") if using named URL
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")  # Redirect to login page after logout


# pearlApp/views.py


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
                user.set_password(password)  # Always hash passwords
            user.save()

            messages.success(request, "Profile updated successfully!")
            return redirect("profile")  # stay on profile page
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "auth/profile.html", {"form": form})

# @login_required
# def profile_view(request):
#     if request.method == "POST":
#         form = UserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect("/profile/")
#     else:
#         form = UserChangeForm(instance=request.user)
#     return render(request, "profile.html", {"form": form})


def orders_view(request):
    return render(request, "stores/orders.html")


def wishlist_view(request):
    return render(request, "stores/wishlist.html")


def cart_view(request):
    return render(request, "stores/cart.html")


def terms_view(request):
    return render(request, "generic/terms.html")


def reset_password_view(request):
    return render(request, "auth/reset_password.html")
