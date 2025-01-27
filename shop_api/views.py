from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from shop_api.mixins import ProductQuerysetMixin
from shop_api.models import Category
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Category model.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class ProductListCreateAPIView(ProductQuerysetMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    serializer_class = ProductSerializer


class ProductDetailAPIView(ProductQuerysetMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    lookup_field = "pk"
