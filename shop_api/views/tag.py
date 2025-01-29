from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from shop_api.models import Tag
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers.tag import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    # filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
