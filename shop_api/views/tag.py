from django.db.models.aggregates import Count
from rest_framework import generics

from shop_api.models import Product, Tag
from shop_api.paginators import ProductsPagination
from shop_api.serializers import ProductSerializer, TagSerializer


class TagProductsListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination

    def get_queryset(self):
        products = Product.objects.filter(
            tags__id=self.kwargs["tag_id"]
        ).prefetch_related("tags", "category")
        return products


class TagListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    # queryset = Tag.objects.prefetch_related("product_set")
    queryset = Tag.objects.annotate(product_count=Count('product_set'))


class TagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.annotate(product_count=Count('product_set'))
