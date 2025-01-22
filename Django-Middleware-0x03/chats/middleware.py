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