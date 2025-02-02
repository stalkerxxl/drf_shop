from rest_framework import serializers

from shop_api.models import Category, Product, Tag


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    # noinspection PyUnresolvedReferences
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "products_count",
        )

    @staticmethod
    def get_products_count(obj):
        return Product.objects.filter(category=obj).count()


class TagSerializer(serializers.HyperlinkedModelSerializer):
    product_count = serializers.SerializerMethodField()

    # noinspection PyUnresolvedReferences
    class Meta:
        model = Tag
        fields = [
            "url",
            "id",
            "name",
            "product_count",
        ]
        extra_kwargs = {"url": {"view_name": "tag-detail", "lookup_field": "pk"}}

    def get_product_count(self, obj: Tag):
        request = self.context.get("request")
        if request and request.user.is_staff:
            return obj.product_set.count()
        return obj.product_set.filter(is_active=True).count()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "in_stock",
            # "image",
            "is_active",
            "category_id",
            "category_name",
        )

    @staticmethod
    def get_category_id(obj: Product):
        return obj.category.id

    @staticmethod
    def get_category_name(obj: Product):
        return obj.category.name
