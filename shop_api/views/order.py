# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
#
# from shop_api.models import Order
# from shop_api.serializers import OrderSerializer
#
#
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
