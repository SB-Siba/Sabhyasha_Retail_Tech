from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

class DebugRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if response.status_code == 302:  # Redirect happening
            logger.warning(f"Redirecting {request.path} → {response['Location']}")
        
        return response
