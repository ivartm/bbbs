# import os
from pprint import pprint

from django.urls import reverse
from mailjet_rest import Client


def send_token(instance, reset_password_token):
    # api_key = os.environ['MJ_APIKEY_PUBLIC']
    # api_secret = os.environ['MJ_APIKEY_PRIVATE']
    api_key = "845e5b1defbbccddbccdc98ca43ca5b5"
    api_secret = "f1fb193800a4dea9e3f534a929d20965"
    mailjet = Client(auth=(api_key, api_secret), version="v3.1")
    print(reset_password_token.user.email)
    data = {
        "Messages": [
            {
                "From": {
                    "Email": "bbbs@kiryanov.ru",
                    "Name": "Служба поддержки BBBS",
                },
                "To": [
                    {
                        "Email": reset_password_token.user.email,
                        "Name": reset_password_token.user.username,
                    }
                ],
                "TemplateID": 3020841,
                "TemplateLanguage": True,
                "Subject": "BBBS, письма для подтверждения регистрации",
                "Variables": {
                    "code": " Код для восстановления "
                    f"{reset_password_token.key}",
                    "reset_link": "{}?token={}".format(
                        instance.request.build_absolute_uri(
                            reverse("password_reset:reset-password-confirm")
                        ),
                        reset_password_token.key,
                    ),
                },
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    pprint(result.json())
