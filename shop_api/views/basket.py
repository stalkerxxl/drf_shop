from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop_api.models import Basket, BasketItem, Product
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

    @action(detail=False, methods=["post"], url_path="add-or-update-item")
    def add_or_update_item(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            raise ValidationError({"error": "Product ID is required"})

        product = Product.objects.get(id=product_id)

        basket, created = self.get_queryset().get_or_create(user=user)
        # fixme валидация quantity (>0)
        # fixme sql-optimize
        basket_item, item_created = BasketItem.objects.get_or_create(
            basket=basket, product=product, defaults={"quantity": quantity}
        )

        if not item_created:
            basket_item.quantity += quantity
            basket_item.save()

        serializer = self.get_serializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="remove-item")
    def remove_item(self, request, pk=None):
        basket = self.get_object()
        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            basket_item = BasketItem.objects.get(basket=basket, product_id=product_id)
            basket_item.delete()
            serializer = self.get_serializer(basket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BasketItem.DoesNotExist:
            return Response(
                {"error": "Product not found in basket"},
                status=status.HTTP_404_NOT_FOUND,
            )
