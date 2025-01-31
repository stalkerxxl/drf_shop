from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from shop_api.models import Category, Product
from shop_api.serializers import CategorySerializer, ProductSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class CategoryProductsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class CategoryProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CategoryProductsPagination

    def get_queryset(self):
        category_id = self.kwargs.get("pk")
        return Product.objects.filter(category_id=category_id)
