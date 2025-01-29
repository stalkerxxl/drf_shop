from rest_framework import serializers

from shop_api.models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    product_count = serializers.SerializerMethodField()

    # noinspection PyUnresolvedReferences
    class Meta:
        model = Tag
        fields = ["url", "id", "name", "created_at", "updated_at", "product_count"]
        extra_kwargs = {"url": {"view_name": "tag-detail", "lookup_field": "pk"}}

    def get_product_count(self, obj: Tag):
        request = self.context.get("request")
        if request and request.user.is_staff:
            return obj.product_set.count()
        return obj.product_set.filter(is_active=True).count()
