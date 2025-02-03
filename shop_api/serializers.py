from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from shop_api.models import Category, Product, Tag


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "product_count",
        )

    # fixme заменить на ProductCountMixin
    @staticmethod
    def get_product_count(obj: Category):
        return obj.product_set.count()


class TagSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "product_count",
        ]

    # fixme заменить на ProductCountMixin
    def get_product_count(self, obj: Tag):
        request = self.context.get("request")
        if request and request.user.is_staff:
            return obj.product_set.count()
        return obj.product_set.filter(is_active=True).count()


class ProductSerializer(serializers.ModelSerializer):
    category = PrimaryKeyRelatedField(many=False, queryset=Category.objects.all())
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

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
            "category",
            "tags",
        )
