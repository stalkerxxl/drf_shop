from rest_framework import permissions, viewsets

from shop_api.models import Comment
from shop_api.paginators import CommentsPagination
from shop_api.permissions import IsOwnerEditOrReadOnly
from shop_api.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerEditOrReadOnly,
    )
    pagination_class = CommentsPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
