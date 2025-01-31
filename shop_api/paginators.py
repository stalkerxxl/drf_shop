from rest_framework.pagination import PageNumberPagination


class ProductsPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
