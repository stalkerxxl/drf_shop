from abc import ABC

from rest_framework.pagination import PageNumberPagination


class BasePagination(ABC, PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class ProductsPagination(BasePagination):
    pass


class CommentsPagination(BasePagination):
    pass


class TagsPagination(BasePagination):
    pass


class CategoriesPagination(BasePagination):
    pass
