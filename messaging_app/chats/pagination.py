from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """Custom pagination for the messages with a page size of 20."""
    page_size = 20