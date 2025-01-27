from rest_framework import serializers

from shop_api.models import Category, Product


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    product_count = serializers.SerializerMethodField()

    # noinspection PyUnresolvedReferences
    class Meta:
        model = Category
        fields = ["url", "id", "name", "created_at", "updated_at", "product_count"]
        extra_kwargs = {"url": {"view_name": "category-detail", "lookup_field": "pk"}}

    @staticmethod
    def get_product_count(obj):
        return Product.objects.filter(category=obj).count()
