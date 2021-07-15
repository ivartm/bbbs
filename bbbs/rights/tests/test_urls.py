from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from bbbs.common.factories import CityFactory
from bbbs.rights.factories import RightFactory, RightTagFactory
from bbbs.users.factories import UserFactory


class UrlRightsAppTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.path_rights = reverse("rights-list")
        cls.path_righttags = reverse("right-tags")
        cls.tag = RightTagFactory(name="?Петровна?")
        cls.right = RightFactory(tags__num=2)

        cls.city = CityFactory(name="Билибино")
        cls.mentor = UserFactory()

        cls.unauthorized_client = APIClient()

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def url_returns_405_not_allowed_test_utility(
        self, client, url, method_names
    ):
        """Helper. Tests "url" for not allowed methods.
        It translates "methods_names" to correspond methods on "client" and
        asserts when error different from 405 (not allowed) returns.
        """

        for method_name in method_names:
            with self.subTest(method_name):
                method = getattr(client, method_name)
                response = method(url)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                    msg=(
                        f"Убедитесь, что для '{url}' "
                        f"метод '{method_name}' запрещен и возвращает "
                        f"правильный номер ошибки."
                    ),
                )

    def url_returns_404_not_found_test_utility(
        self, client, url, method_names
    ):
        """Helper. Tests "url" for 404 with provided methods.
        It translates "methods_names" to correspond methods on "client" and
        asserts when error different from 404 (not found) returns.
        """

        for method_name in method_names:
            with self.subTest(method_name):
                method = getattr(client, method_name)
                response = method(url)

                self.assertEqual(
                    response.status_code,
                    status.HTTP_404_NOT_FOUND,
                    msg=(
                        f"Убедитесь, для индивидуальных URL, таких как"
                        f"'{url}' при запросе методом '{method_name}'"
                        f"возвращается ошибка 404"
                    ),
                )

    def test_rights_get_response_status_code(self):
        """Unauthorized user and mentor have access to Right list."""
        user = UrlRightsAppTests.mentor
        authorized_client = self.return_authorized_user_client(user)
        clients = [
            UrlRightsAppTests.unauthorized_client,
            authorized_client,
        ]
        for client in clients:
            with self.subTest(client):
                response = client.get(UrlRightsAppTests.path_rights)
                self.assertEqual(response.status_code, 200)

    # def test_right_individual_urls_return_404(self):
    #     method_to_test = [
    #         "get",
    #         "patch",
    #         "post",
    #         "put",
    #         "delete",
    #     ]
    #     right_id = UrlRightsAppTests.right.id
    #     individual_right_url = UrlRightsAppTests.path_rights + str(right_id)

    #     client = self.return_authorized_user_client(UrlRightsAppTests.mentor)

    #     self.url_returns_404_not_found_test_utility(
    #         client=client,
    #         url=individual_right_url,
    #         method_names=method_to_test,
    #     )

    # def test_righttags_individual_urls_return_404(self):
    #     method_to_test = [
    #         "get",
    #         "patch",
    #         "post",
    #         "put",
    #         "delete",
    #     ]
    #     tag_id = UrlRightsAppTests.tag.id
    #     individual_tag_url = UrlRightsAppTests.path_rights + str(tag_id)

    #     client = self.return_authorized_user_client(UrlRightsAppTests.mentor)

    #     self.url_returns_404_not_found_test_utility(
    #         client=client,
    #         url=individual_tag_url,
    #         method_names=method_to_test,
    #     )

    def test_rights_list_returns_405_not_allowed_method(self):
        """Runs with authorized user. Unauthorized may return 401 error."""
        not_allowed_method_names = [
            "patch",
            "post",
            "put",
            "delete",
        ]
        rights_url = UrlRightsAppTests.path_rights

        client = self.return_authorized_user_client(UrlRightsAppTests.mentor)

        self.url_returns_405_not_allowed_test_utility(
            client=client,
            url=rights_url,
            method_names=not_allowed_method_names,
        )

    def test_righttags_list_returns_405_not_allowed_method(self):
        """Runs with authorized user. Unauthorized may return 401 error."""
        not_allowed_method_names = [
            "patch",
            "post",
            "put",
            "delete",
        ]
        tags_url = UrlRightsAppTests.path_righttags

        client = self.return_authorized_user_client(UrlRightsAppTests.mentor)

        self.url_returns_405_not_allowed_test_utility(
            client=client,
            url=tags_url,
            method_names=not_allowed_method_names,
        )
