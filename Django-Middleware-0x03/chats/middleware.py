import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        Initialize the middleware. The `get_response` is the next layer of middleware
        that will be called after this one.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        This method is called on each request. We log the user and path here.
        """
        # Get the user (if authenticated) and request path
        user = request.user if request.user.is_authenticated else "Anonymous"
        path = request.path

        # Prepare the log message
        log_message = f"{datetime.now()} - User: {user} - Path: {path}"

        # Log to a file
        self.log_request(log_message)

        # Call the next middleware or view
        response = self.get_response(request)

        return response

    def log_request(self, log_message):
        """
        Log the request details to a file.
        """
        with open('requests.log', 'a') as log_file:
            log_file.write(log_message + '\n')

    class RestrictAccessByTimeMiddleware:
        def __init__(self, get_response):
            """
            Initialize the middleware. The `get_response` is the next middleware
            that will be called after this one.
            """
            self.get_response = get_response

    def __call__(self, request):
        """
        This method checks the current time and restricts access to the chat app
        if the request is made outside the allowed hours (9 AM to 6 PM).
        """
        current_time = datetime.now().hour  # Get the current hour
        
        # Restrict access if the time is not between 9 AM and 6 PM
        if current_time < 9 or current_time >= 18:
            return HttpResponseForbidden("Access to the chat is restricted between 6 PM and 9 AM.")

        # Call the next middleware or view
        response = self.get_response(request)
        return response
    class OffensiveLanguageMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response
            self.requests_log = {}  # To track messages per IP

    def __call__(self, request):
        # Only count POST requests (assumed to be sending chat messages)
        if request.method == 'POST':
            client_ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize or clean up old entries
            if client_ip not in self.requests_log:
                self.requests_log[client_ip] = []
            self.requests_log[client_ip] = [
                timestamp for timestamp in self.requests_log[client_ip]
                if timestamp > now - timedelta(minutes=1)
            ]

            # Check if the user exceeds the limit
            if len(self.requests_log[client_ip]) >= 5:
                return JsonResponse(
                    {'error': 'Message limit exceeded. Try again later.'},
                    status=429
                )

            # Add current request time to the log
            self.requests_log[client_ip].append(now)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        # Get client IP from request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
    class RolePermissionMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        # Check the user's role only for specific actions
        if '/restricted-action/' in request.path:  # Replace with your restricted path
            user = request.user  # Assuming user is attached to the request
            if not user.is_authenticated or user.role not in ['admin', 'moderator']:
                return JsonResponse(
                    {'error': 'Access denied. Insufficient permissions.'},
                    status=403
                )
        return self.get_response(request)