from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action

from shop_api.filters import OnlyActiveProductsFilter
from shop_api.models import Product, Comment
from shop_api.paginators import ProductsPagination
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers import ProductSerializer, CommentSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("category", "tags").annotate(
        comments_count=Count("comments")
    )
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = ProductsPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        OnlyActiveProductsFilter,
    )
    search_fields = ["name", "description", "category__name", "tags__name"]
    ordering_fields = ["name", "price", "in_stock"]

    @action(
        detail=True,
        methods=["get"],
        url_path="comments",
        url_name="comments",
        name="Comments for product",
        description="Get all comments for the product",
        serializer_class=CommentSerializer,
        queryset=Comment.objects.all(),
        filter_backends=(OnlyActiveProductsFilter,),
    )
    def comments_list(self, request, pk=None):
        self.queryset = self.get_queryset().filter(product_id=pk)
        return self.list(request)
