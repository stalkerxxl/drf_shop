from rest_framework import serializers
from rest_framework.generics import GenericAPIView

from shop_api.models import Product


class ProductQuerysetMixin(GenericAPIView):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Product.objects.all()
        return Product.objects.active()


class ProductCountMixin(serializers.Serializer):
    def get_product_count(self, obj):
        request = self.context.get("request")
        if request and request.user.is_staff:
            return obj.product_set.count()
        return obj.product_set.filter(is_active=True).count()
