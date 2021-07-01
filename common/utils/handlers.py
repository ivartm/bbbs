from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        "ValidationError": _handle_validation_error,
        "ParseError": _handle_drf_general_error,
        "AuthenticationFailed": _handle_drf_general_error,
        "NotAuthenticated": _handle_drf_general_error,
        "PermissionDenied": _handle_drf_general_error,
        "NotFound": _handle_drf_general_error,
        "MethodNotAllowed": _handle_drf_general_error,
        "NotAcceptable": _handle_drf_general_error,
        "UnsupportedMediaType": _handle_drf_general_error,
        "Throttled": _handle_drf_general_error,
        "CityNotSelected": _handle_unknown_general_error,
    }

    response = exception_handler(exc, context)
    if response is not None:
        exception_class = exc.__class__.__name__
        if exception_class in handlers:
            return handlers[exception_class](exc, context, response)

    return _handle_unknown_general_error(exc, context, response)


def _handle_validation_error(exc, context, response):
    response.data = {
        "message": "Отправленные данные не прошли проверку",
        "errors": response.data,
    }
    return response


def _handle_drf_general_error(exc, context, response):
    # message = response.data["detail"]
    # errors = response.data
    response.data = {
        "message": response.data["detail"],
        "errors": response.data,
    }
    return response


def _handle_unknown_general_error(exc, context, response):
    # message = response.data["detail"]
    # errors = response.data
    response.data = {
        "message": exc.__class__.__name__,
        "errors": response.data,
    }
    return response
