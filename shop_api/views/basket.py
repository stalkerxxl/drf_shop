from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from shop_api.models import Basket
from shop_api.serializers import BasketSerializer


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.prefetch_related(
        "basketitem_set__product",
        "basketitem_set__product__tags",
        "basketitem_set__product__category",
    )
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: BasketSerializer):
        serializer.save(user=self.request.user)
