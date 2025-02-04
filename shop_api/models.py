from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    def __str__(self):
        return self.username


class Category(TimestampMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(TimestampMixin, models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def active(self):
        return self.get_queryset().filter(is_active=True)


class Product(TimestampMixin, models.Model):
    objects = ProductManager()

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)]
    )
    in_stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    is_active = models.BooleanField(default=False)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product_set"
    )
    tags = models.ManyToManyField(Tag, related_name="product_set")

    def __str__(self):
        return self.name


class Comment(TimestampMixin, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500, blank=False)

    # simple way to prevent duplicate comments
    class Meta:
        unique_together = ['user', 'text']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}: {self.text[:50]}"
