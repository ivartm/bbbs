from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        "ValidationError": _handle_validation_error,
        "Http404": _handle_not_found_error,
    }

    response = exception_handler(exc, context)
    if response is not None:
        exception_class = exc.__class__.__name__
        if exception_class in handlers:
            return handlers[exception_class](exc, context, response)

        return _handle_drf_general_error(exc, context, response)


def _handle_validation_error(exc, context, response):
    """Generic error for 'ValidationError' exception."""
    response.data = {
        "error": "ValidationError",
        "message": "Отправленные данные не прошли проверку",
        "details": response.data,
    }
    return response


def _handle_not_found_error(exc, context, response):
    """Generic error for 'get_object_or_404()' function."""
    response.data = {
        "error": "NotFound",
        "message": "Запрошенный объект не найден",
    }
    return response


def _handle_drf_general_error(exc, context, response):
    """Generic handler for DRF exceptions. Expects 'detail' in response."""
    response.data = {
        "error": exc.__class__.__name__,
        "message": response.data.get("detail"),
    }
    return response
