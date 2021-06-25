from rest_framework.exceptions import APIException


class CityNotSelected(APIException):
    status_code = 500
    default_detail = "Пожалуйста, выберите город."
