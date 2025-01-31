from django.urls import path

from shop_api.views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    CategoryListAPIView,
    CategoryDetailAPIView,
)

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="categories-list"),
    path(
        "categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"
    ),
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
]
