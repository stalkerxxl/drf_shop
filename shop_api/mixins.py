from rest_framework.generics import GenericAPIView

from shop_api.models import Product


class ProductQuerysetMixin(GenericAPIView):

    def get_queryset(self):
        if self.request.user.is_staff:
            return Product.objects.all()
        return Product.objects.active()
