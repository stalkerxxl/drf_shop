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
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=500, blank=False)
    # simple way to prevent duplicate comments
    class Meta:
        unique_together = ["user", "text"]

    def __str__(self):
        return f"{self.user.username} - {self.product.name}: {self.text[:50]}"


class Basket(TimestampMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="basket")
    items = models.ManyToManyField(Product, through="BasketItem")

    def __str__(self):
        return f"{self.user.username} - Basket {self.id}"


class BasketItem(TimestampMixin, models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ["basket", "product"]

    @property
    def sum(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.basket.id}: {self.product.name} * {self.quantity} products"

# class Order(TimestampMixin, models.Model):
#     class Status(models.TextChoices):
#         CREATED = "created"
#         PAID = "paid"
#         SHIPPED = "shipped"
#         DELIVERED = "delivered"
#         CANCELED = "canceled"
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
#     products = models.ManyToManyField(Product, through="OrderItem")
#     status = models.CharField(max_length=20, choices=Status, default=Status.CREATED)
#
#     def __str__(self):
#         return f"{self.user.username} - Order {self.id}: {self.status}"
#
#
# class OrderItem(TimestampMixin, models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
#     sum = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#
#     class Meta:
#         unique_together = ["order", "product"]
#
#     def save(self, *args, **kwargs):
#         self.sum = self.price * self.quantity
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.order.id}: {self.product.name}, {self.price} * {self.quantity} products"
