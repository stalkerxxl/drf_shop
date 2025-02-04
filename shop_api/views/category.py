from django.db.models import QuerySet
from django.db.models.aggregates import Count
from rest_framework import viewsets
from rest_framework.decorators import action

from shop_api.filters import OnlyActiveProductsFilter
from shop_api.models import Category, Product
from shop_api.paginators import ProductsPagination
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(product_count=Count("product_set"))
    permission_classes = (IsAdminOrReadOnly,)

    @action(
        detail=True,
        methods=["get"],
        url_path="products",
        url_name="products",
        name="Products by category",
        description="Get all products for the category",
        serializer_class=ProductSerializer,
        pagination_class=ProductsPagination,
        queryset=Product.objects.prefetch_related("tags", "category"),
        filter_backends=(OnlyActiveProductsFilter,)
    )
    def products_list(self, request, pk=None):
        self.queryset: QuerySet[Product] = self.get_queryset().filter(category_id=pk)
        return self.list(request)

# class CategoryListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     pagination_class = None
#     permission_classes = [IsAdminOrReadOnly]
#
#
# class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminOrReadOnly]
#
#     def get_queryset(self):
#         if self.request.method == "GET":
#             return Category.objects.prefetch_related("product_set__tags")
#         return Category.objects.all()
#
#     def retrieve(self, request, *args, **kwargs):
#         category: Category = self.get_object()
#         products = category.product_set.all()
#         paginator = ProductsPagination()
#         page = paginator.paginate_queryset(products, request)
#         product_serializer = ProductSerializer(page, many=True)
#
#         response_data = {
#             "category": self.get_serializer(category).data,
#             "products": paginator.get_paginated_response(product_serializer.data).data,
#         }
#         return Response(response_data)
