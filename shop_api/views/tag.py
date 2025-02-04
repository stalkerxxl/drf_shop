from django.db.models.aggregates import Count
from rest_framework import viewsets
from rest_framework.decorators import action

from shop_api.filters import OnlyActiveProductsFilter
from shop_api.models import Product, Tag
from shop_api.paginators import ProductsPagination
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers import ProductSerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.annotate(product_count=Count("product_set"))
    permission_classes = (IsAdminOrReadOnly,)

    @action(
        detail=True,
        methods=["get"],
        url_path="products",
        url_name="products",
        name="Products by tag",
        description="Get all products for the tag",
        serializer_class=ProductSerializer,
        pagination_class=ProductsPagination,
        queryset=Product.objects.prefetch_related("tags", "category"),
        filter_backends=(OnlyActiveProductsFilter,)
    )
    def products_list(self, request, pk=None):
        self.queryset = self.get_queryset().filter(tags__id=pk)
        return self.list(request)
