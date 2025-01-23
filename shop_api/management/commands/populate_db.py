import random

from django.core.management.base import BaseCommand

from shop_api.models import Category, Product, Tag


class Command(BaseCommand):
    help = "Populate the database with fake data"

    def __init__(self):
        super().__init__()
        self.tags = []
        self.categories = []
        self.products = []

    def handle(self, *args, **kwargs):
        self.clear_database()
        self.create_categories()
        self.create_tags()
        self.create_products()
        self.assign_tags_to_products()

        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with fake data")
        )

    def create_categories(self):
        for i in range(1, 6):
            category = Category.objects.create(name=f"Category {i}")
            self.categories.append(category)

    def create_tags(self):
        for i in range(1, 6):
            tag = Tag.objects.create(name=f"Tag {i}")
            self.tags.append(tag)

    def create_products(self):
        for i in range(1, 21):
            product = Product.objects.create(
                name=f"Product {i}",
                description=f"Description for product {i}",
                price=round(random.uniform(2, 100), 2),
                category=self.categories[(i - 1) % 5],
                in_stock=random.randint(5, 50),
                is_active=True,
            )
            self.products.append(product)

    def assign_tags_to_products(self):
        for product in random.sample(self.products, 10):
            tags = random.sample(self.tags, random.randint(1, 2))
            product.tags.set(tags)

    @staticmethod
    def clear_database():
        Product.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
