from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from shop_api.models import Category, Product
from shop_api.permissions import IsAdminOrReadOnly
from shop_api.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Category model.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class ProductListCreateAPIView(APIView):
    """
    Представление для получения списка продуктов и создания нового продукта.
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get(self, request):
        if request.user.is_staff:
            products = Product.objects.all()
        else:
            products = Product.objects.active()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    """
    Представление для получения, обновления и удаления конкретного продукта.
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            if self.request.user.is_staff:
                return Product.objects.get(pk=pk)
            else:
                return Product.objects.active().get(pk=pk)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
