from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FlexiblePageNumberPagination(PageNumberPagination):
    """
    Flexible pagination that allows users to control page size.
    Supports large page sizes for bulk data export while maintaining reasonable defaults.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000  # Allow up to 10K records per page for bulk operations
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.page.paginator.per_page,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })