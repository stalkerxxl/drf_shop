from rest_framework import serializers

from shop_api.models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    product_count = serializers.SerializerMethodField()

    # noinspection PyUnresolvedReferences
    class Meta:
        model = Tag
        fields = ["url", "id", "name", "created_at", "updated_at", "product_count"]
        extra_kwargs = {"url": {"view_name": "tag-detail", "lookup_field": "pk"}}

    @staticmethod
    def get_product_count(obj: Tag):
        return obj.product_set.count()
