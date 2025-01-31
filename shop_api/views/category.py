from rest_framework import generics
from rest_framework.response import Response

from shop_api.models import Category
from shop_api.paginators import CategoryProductsPagination
from shop_api.serializers import CategorySerializer, ProductSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.prefetch_related("product_set")
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        category: Category = self.get_object()
        products = category.product_set.all()
        paginator = CategoryProductsPagination()
        page = paginator.paginate_queryset(products, request)
        product_serializer = ProductSerializer(page, many=True)

        response_data = {
            "category": self.get_serializer(category).data,
            "products": paginator.get_paginated_response(product_serializer.data).data,
        }
        return Response(response_data)
