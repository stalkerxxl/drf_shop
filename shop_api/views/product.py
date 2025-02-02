from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from shop_api.mixins import ProductQuerysetMixin
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers import ProductSerializer


class ProductListCreateAPIView(ProductQuerysetMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination


class ProductDetailAPIView(ProductQuerysetMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    lookup_field = "pk"
