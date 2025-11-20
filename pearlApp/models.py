from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, contact, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, contact=contact, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, contact, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, contact, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["contact"]

    objects = UserManager()


# ================= Category Model =================

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(
        unique=True, help_text="URL-friendly name for the category"
    )
    image = models.ImageField(
        upload_to="category_images/",
        blank=True,
        null=True,
        help_text="Optional image to represent the category"
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    # Auto-generate slug if not provided
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ================= Product Model =================
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.PositiveIntegerField(help_text="Price in UGX")
    discount = models.PositiveIntegerField(
        default=0, help_text="Discount percentage (0 if none)")
    image = models.ImageField(upload_to="products/")
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        """Return price after discount"""
        if self.discount > 0:
            return self.price - (self.price * self.discount // 100)
        return self.price

    @property
    def stock_display(self):
        """Display stock with appropriate unit"""
        unit = "pieces"  # You can later customize per category if needed
        return f"{self.stock_quantity} {unit} remaining"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        if self.product.discount:
            return self.quantity * self.product.discounted_price
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
