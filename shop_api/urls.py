from django.urls import path

from shop_api.views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView, TagProductsListAPIView, TagListCreateAPIView,
)

urlpatterns = [
    path(
        "categories/",
        CategoryListCreateAPIView.as_view(),
        name="categories-list-create",
    ),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdateDestroyAPIView.as_view(),
        name="category-retrieve-update-destroy",
    ),
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),

    path("tags/<int:tag_id>/products/", TagProductsListAPIView.as_view(),
         name="tag-products-list"),
    path("tags/", TagListCreateAPIView.as_view(), name="tag-list-create"),
]
