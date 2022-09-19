
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 500