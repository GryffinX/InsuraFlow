import time
import logging

logger = logging.getLogger(__name__)

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        duration = time.time() - start_time
        response_ms = duration * 1000

        user_id = request.user.id if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'

        # Log the request details
        log_data = (
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"Status: {response.status_code} | "
            f"User: {user_id} | "
            f"Duration: {response_ms:.2f}ms"
        )
        
        if response.status_code >= 500:
            logger.error(log_data)
        elif response.status_code >= 400:
            logger.warning(log_data)
        else:
            logger.info(log_data)

        return response
