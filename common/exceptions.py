from rest_framework import status
from rest_framework.exceptions import APIException


class CityNotSelected(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = (
        "Запросы от неавторизованных пользователей должны содержать query "
        "параметр города (city)"
    )
