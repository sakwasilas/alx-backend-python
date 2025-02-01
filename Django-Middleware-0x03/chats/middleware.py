import logging
from datetime import datetime, time, timedelta
from django.http import JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        Middleware initialization. Called only once when the server starts.
        """
        self.get_response = get_response
        # Configure the logger
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s",
        )

    def __call__(self, request):
        """
        Middleware logic executed for each request.
        """
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        """
        Middleware initialization. Called only once when the server starts.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Middleware logic executed for each request.
        Restricts access to chats outside 6 PM to 9 PM.
        """
        # Define the restricted hours
        start_time = time(21, 0)  # 9 PM
        end_time = time(18, 0)   # 6 PM

        # Get the current server time
        current_time = datetime.now().time()

        # Check if the current time is outside the allowed range
        if not (end_time <= current_time <= start_time):
            return JsonResponse(
                {
                    "error": "Access to the chat is restricted outside 9 PM and 6 PM."
                },
                status=403
            )

        # Proceed with the request if time is allowed
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware to track and limit chat messages based on IP address.
    """
    def __init__(self, get_response):
        """
        Initialize the middleware and set up storage for IP tracking.
        """
        self.get_response = get_response
        self.message_limits = {}  # Store message counts and timestamps per IP
        self.TIME_WINDOW = timedelta(minutes=1)  # 1-minute time window
        self.MAX_MESSAGES = 5  # Max 5 messages per time window

    def __call__(self, request):
        """
        Handle incoming requests and enforce message limits.
        """
        # Only apply limits to POST requests (e.g., sending messages)
        if request.method == 'POST':
            ip_address = self.get_client_ip(request)

            # Initialize or update the user's message data
            now = datetime.now()
            if ip_address not in self.message_limits:
                self.message_limits[ip_address] = {"count": 1, "start_time": now}
            else:
                user_data = self.message_limits[ip_address]
                elapsed_time = now - user_data["start_time"]

                if elapsed_time < self.TIME_WINDOW:
                    # Within the time window
                    if user_data["count"] >= self.MAX_MESSAGES:
                        return JsonResponse(
                            {"error": "Message limit exceeded. Try again later."},
                            status=429  # Too Many Requests
                        )
                    user_data["count"] += 1
                else:
                    # Time window has expired, reset the counter
                    self.message_limits[ip_address] = {"count": 1, "start_time": now}

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """
        Retrieve the client's IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    """
    Middleware to enforce role-based permissions for users.
    """
    def __init__(self, get_response):
        """
        Initialize the middleware.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Check the user's role and enforce permissions.
        """
        # List of roles allowed to perform restricted actions
        allowed_roles = ['admin', 'moderator']

        # Assuming user role is passed in the request header for simplicity
        # In a real app, you'd use request.user and their associated roles
        user_role = request.headers.get('X-User-Role')

        # Define restricted actions (e.g., POST or DELETE requests)
        restricted_methods = ['POST', 'DELETE']

        if request.method in restricted_methods and user_role not in allowed_roles:
            return JsonResponse(
                {"error": "Access denied. Admin or moderator role required."},
                status=403  # Forbidden
            )

        response = self.get_response(request)
        return response
