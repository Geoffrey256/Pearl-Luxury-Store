from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "home.html")


def landing(request):
    return render(request, "generic/land.html")


# SIGNUP VIEW


# def signup_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         contact = request.POST.get("contact")
#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")
#         terms = request.POST.get("terms")  # checkbox

#         # Basic validations
#         if not all([email, contact, password1, password2]):
#             messages.error(request, "Please fill in all fields.")
#             return redirect("signup")

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect("signup")

#         if not terms:
#             messages.error(
#                 request, "You must agree to the Terms and Conditions.")
#             return redirect("signup")

#         try:
#             # Create user
#             user = User.objects.create_user(
#                 username=email,  # using email as username
#                 email=email,
#                 password=password1,
#             )
#             # Optional: save contact in User model's first_name field or create a profile model
#             user.first_name = contact
#             user.save()

#             # Log the user in
#             user = authenticate(request, username=email, password=password1)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "Account created successfully!")
#                 return redirect("landing")  # redirect to home or landing page
#             else:
#                 messages.error(
#                     request, "Something went wrong. Please try logging in.")
#                 return redirect("login")

#         except IntegrityError:
#             messages.error(request, "Email already exists. Please login.")
#             return redirect("login")

#     return render(request, "signup.html")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "auth/signup.html", {"form": form})


# def login_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         remember_me = request.POST.get("remember_me")

#         if not email or not password:
#             messages.error(request, "Please enter both email and password.")
#             return redirect("login")

#         # Authenticate using email as username
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)

#             # Handle "remember me"
#             if remember_me:
#                 # Session expires in 30 days
#                 request.session.set_expiry(60 * 60 * 24 * 30)
#             else:
#                 # Session expires on browser close
#                 request.session.set_expiry(0)

#             messages.success(
#                 request, f"Welcome back, {user.first_name or user.username}!")
#             return redirect("landing")  # Redirect to homepage or landing page
#         else:
#             messages.error(request, "Invalid email or password.")
#             return redirect("login")

#     return render(request, "login.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/profile/")
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, "profile.html", {"form": form})


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
