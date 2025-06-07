import logging
from datetime import datetime
from django.http import HttpResponseForbidden

# Configure logger for RequestLoggingMiddleware
logging.basicConfig(
    filename=str(Path(__file__).resolve().parent.parent.parent / 'requests.log'),
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
        user = request.user if request.user.is_authenticated else 'AnonymousUser'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to the app outside 6 PM to 9 PM."""
    
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Check server time and deny access outside 6 PM to 9 PM."""
        current_hour = datetime.now().hour
        if not (18 <= current_hour < 21):  # 6 PM (18:00) to 9 PM (21:00)
            return HttpResponseForbidden("Access to the messaging app is restricted outside 6 PM to 9 PM.")
        return self.get_response(request)