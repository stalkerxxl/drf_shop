import random

from django.core.management.base import BaseCommand

from core.settings import SUPERUSER_EMAIL, SUPERUSER_USERNAME, SUPERUSER_PASSWORD
from shop_api.models import Category, Product, Tag, User


class Command(BaseCommand):
    """
    A Django management command to populate the database with fake data.
    """

    help = "Populate the database with fake data"

    def __init__(self):
        """
        Initialize the command with empty lists for tags, categories, and products.
        """
        super().__init__()
        self.tags = []
        self.categories = []
        self.products = []

    def handle(self, *args, **kwargs):
        """
        Main entry point for the command. Clears the database and populates it with fake data.
        """
        self.create_superuser()
        self.clear_database()
        self.create_categories()
        self.create_tags()
        self.create_products()
        self.assign_tags_to_products()

        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with fake data")
        )

    def create_categories(self):
        """
        Create 5 categories and store them in the categories list.
        """
        for i in range(1, 6):
            category = Category.objects.create(name=f"Category {i}")
            self.categories.append(category)

    def create_tags(self):
        """
        Create 5 tags and store them in the tags list.
        """
        for i in range(1, 6):
            tag = Tag.objects.create(name=f"Tag {i}")
            self.tags.append(tag)

    def create_products(self):
        """
        Create 20 products, each associated with a category, and store them in the products list.
        """
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
        """
        Assign 1 or 2 random tags to 10 randomly selected products.
        """
        for product in random.sample(self.products, 10):
            tags = random.sample(self.tags, random.randint(1, 2))
            product.tags.set(tags)

    @staticmethod
    def create_superuser():
        """
        Create a superuser with predefined credentials.
        """
        if not User.objects.filter(username="root").exists():
            User.objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD,
            )

    @staticmethod
    def clear_database():
        """
        Clear the database by deleting all products, categories, and tags.
        """
        Product.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
