from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, DjangoValidationError):
        # Handle Django's built-in validation errors
        if hasattr(exc, 'message_dict'):
            data = {"error": "Validation Error", "details": exc.message_dict}
        elif hasattr(exc, 'messages'):
            data = {"error": "Validation Error", "details": exc.messages}
        else:
            data = {"error": "Validation Error", "details": str(exc)}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if response is not None:
        # Reformat standard DRF errors
        custom_response_data = {
            "error": "Error",
            "details": response.data
        }
        
        # Give a better error message if it's an authorization error
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response_data["error"] = "Authentication failed"
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data["error"] = "Permission denied"
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data["error"] = "Not found"
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data["error"] = "Validation Error"

        response.data = custom_response_data
    else:
        # Handle unexpected Python exceptions (internal server errors)
        # Note: In production with DEBUG=False, this avoids exposing traceback
        data = {
            "error": "Internal Server Error",
            "details": str(exc) # In a strict production setting, you might hide the exact string
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
