from django.urls import path
from rest_framework.routers import DefaultRouter

from shop_api.views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
    TagProductsListAPIView,
    TagViewSet,
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
    path(
        "tags/<int:tag_id>/products/",
        TagProductsListAPIView.as_view(),
        name="tag-products-list",
    ),
]

router = DefaultRouter()
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns += router.urls
