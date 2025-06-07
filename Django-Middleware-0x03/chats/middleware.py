import logging
from datetime import datetime

# Configure logger
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    """Middleware to log user requests with timestamp, user, and path."""
    
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Log the request details and process the request."""
        # Get user (authenticated or AnonymousUser)
        user = request.user if request.user.is_authenticated else 'AnonymousUser'
        # Log the request
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        # Process the request
        response = self.get_response(request)
        return response