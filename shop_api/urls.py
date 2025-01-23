from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop_api.views import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
