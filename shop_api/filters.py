from django.db.models import QuerySet
from rest_framework import filters

from shop_api.models import Product


class OnlyActiveProductsFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet[Product], view):
        if request.user.is_staff:
            return queryset
        return queryset.filter(is_active=True)
