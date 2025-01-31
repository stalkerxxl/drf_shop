from django.urls import path

from shop_api.views import (
    ProductListCreateAPIView,
    ProductDetailAPIView, CategoryListAPIView, CategoryProductsAPIView,
)

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("categories/<int:pk>/products/", CategoryProductsAPIView.as_view(),
         name="category-products"),
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
]
