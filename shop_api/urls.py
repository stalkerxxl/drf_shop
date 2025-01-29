from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop_api.views import (
    CategoryViewSet,
    ProductListCreateAPIView,
    ProductDetailAPIView,
)
from shop_api.views.tag import TagViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
]
