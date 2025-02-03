from django.db.models.aggregates import Count
from rest_framework import generics, viewsets

from shop_api.models import Product, Tag
from shop_api.paginators import ProductsPagination
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers import ProductSerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.annotate(product_count=Count("product_set"))
    permission_classes = [IsAdminOrReadOnly]


class TagProductsListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination

    def get_queryset(self):
        products = Product.objects.filter(
            tags__id=self.kwargs["tag_id"]
        ).prefetch_related("tags", "category")
        return products
