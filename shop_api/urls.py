from django.urls import path
from rest_framework.routers import DefaultRouter

from shop_api.views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    TagViewSet,
    CategoryViewSet,
)

urlpatterns = [
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
]

router = DefaultRouter()
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"categories", CategoryViewSet, basename="categories")

urlpatterns += router.urls
