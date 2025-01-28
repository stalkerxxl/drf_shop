from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from shop_api.models import Category
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Category model.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    pagination_class = None
