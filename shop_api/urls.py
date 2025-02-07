from rest_framework.routers import DefaultRouter

from shop_api.views import (
    TagViewSet,
    CategoryViewSet,
    ProductViewSet,
    CommentViewSet,
    BasketViewSet, UserViewSet,
)

urlpatterns = []
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"comments", CommentViewSet, basename="comments")
# router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"baskets", BasketViewSet, basename="basket")
urlpatterns += router.urls
