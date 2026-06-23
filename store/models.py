from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# ============================================================
# CUSTOM USER MANAGER
# This tells Django how to create users for our custom model
# ============================================================
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


# ============================================================
# USER MODEL
# Our custom user — has buyer and seller support
# ============================================================
class User(AbstractBaseUser):
    email           = models.EmailField(max_length=100, unique=True)
    username        = models.CharField(max_length=50, unique=True)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_seller       = models.BooleanField(default=False)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


# ============================================================
# SELLER DETAIL MODEL
# Extra info for seller accounts
# ============================================================
class SellerDetail(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    shop       = models.CharField(max_length=100)
    phone      = models.CharField(max_length=11)
    address    = models.CharField(max_length=200)
    account_no = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.shop}"


# ============================================================
# CATEGORY MODEL
# Product categories like Men, Women, Electronics
# ============================================================
class Category(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='categories/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# ============================================================
# PRODUCTS MODEL
# All products listed by sellers
# ============================================================
class Products(models.Model):
    seller      = models.ForeignKey(User, on_delete=models.CASCADE)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    productName = models.CharField(max_length=200)
    brand       = models.CharField(max_length=100)
    price       = models.PositiveIntegerField()
    quantity    = models.PositiveIntegerField()
    description = models.TextField()
    image1      = models.ImageField(upload_to='products/')
    image2      = models.ImageField(upload_to='products/', blank=True)
    image3      = models.ImageField(upload_to='products/', blank=True)
    image4      = models.ImageField(upload_to='products/', blank=True)
    date_added  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName

    class Meta:
        verbose_name_plural = "Products"


# ============================================================
# CART MODEL
# Items buyer has added to cart
# ============================================================
class Cart(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    qty     = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.productName}"


# ============================================================
# ORDER MODEL
# A placed order by buyer
# ============================================================
class Order(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid   = models.BooleanField(default=False)
    date      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


# ============================================================
# ORDER DETAILS MODEL
# Individual products inside each order
# ============================================================
class OrderDetails(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE)
    product    = models.ForeignKey(Products, on_delete=models.CASCADE)
    qty        = models.PositiveIntegerField()
    is_shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.productName}"


# ============================================================
# PRODUCT REVIEW MODEL
# Star ratings and reviews by buyers
# ============================================================
class ProductReview(models.Model):
    product    = models.ForeignKey(Products, on_delete=models.CASCADE)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    subject    = models.CharField(max_length=200)
    content    = models.TextField()
    rate       = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.rate} stars"