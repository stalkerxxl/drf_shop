from rest_framework import viewsets

from shop_api.models import Product
from shop_api.paginators import ProductsPagination
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("category", "tags")
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ProductsPagination
