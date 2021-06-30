from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from common.factories import CityFactory
from places.factories import PlaceFactory, PlacesTagFactory
from places.models import Place
from users.factories import UserFactory
from users.models import Profile


class ViewPlacesTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.city = CityFactory(name="Тула")
        cls.mentor = UserFactory(
            profile__role=Profile.Role.MENTOR,
            profile__city=cls.city,
        )
        cls.moderator_reg = UserFactory(
            profile__role=Profile.Role.MODERATOR_REG,
            profile__city=cls.city,
        )
        cls.moderator_gen = UserFactory(
            profile__role=Profile.Role.MODERATOR_GEN,
            profile__city=cls.city,
        )
        cls.admin = UserFactory(
            profile__role=Profile.Role.ADMIN,
            profile__city=cls.city,
        )
        cls.unauthorized_client = APIClient()

        cls.authorized_users = [
            cls.mentor,
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
        ]

        cls.all_users = [
            cls.mentor,
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
            cls.unauthorized_client,
        ]

        cls.path_places = reverse("places")
        cls.path_query_places = cls.path_places + f"?city={cls.city.id}"

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_places_correct_fields_unauthorized_client(self):
        client = ViewPlacesTests.unauthorized_client
        PlaceFactory.create_batch(10)
        response = client.get(ViewPlacesTests.path_query_places).data
        self.assertTrue("count" in response)
        self.assertTrue("next" in response)
        self.assertTrue("previous" in response)
        self.assertTrue("results" in response)

        fields = [
            "id",
            "info",
            "tags",
            "chosen",
            "title",
            "city",
            "address",
            "description",
            "link",
            "imageUrl",
        ]
        results = response.get("results")[0]
        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in results, msg=f"Нет поля {field}")

    def test_places_correct_fields_authorized_client(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)
        PlaceFactory.create_batch(10)
        response = client.get(ViewPlacesTests.path_places).data
        self.assertTrue("count" in response)
        self.assertTrue("next" in response)
        self.assertTrue("previous" in response)
        self.assertTrue("results" in response)

        fields = [
            "id",
            "info",
            "tags",
            "chosen",
            "title",
            "address",
            "city",
            "description",
            "link",
            "imageUrl",
        ]
        results = response.get("results")[0]
        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in results, msg=f"Нет поля {field}")

    def test_places_list_context(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)
        PlaceFactory.create_batch(30)
        response = client.get(ViewPlacesTests.path_places).data
        self.assertEqual(response["count"], 30)

        results = response.get("results")[0]
        obj = Place.objects.get(pk=1)
        self.assertEqual(results["id"], obj.pk)
        # Поле инфо проверю отдельным методом
        # Теги тоже
        self.assertEqual(results["chosen"], obj.chosen)
        self.assertEqual(results["title"], obj.title)
        self.assertEqual(results["address"], obj.address)
        self.assertEqual(results["city"], obj.city.id)
        self.assertEqual(results["description"], obj.description)
        self.assertEqual(results["link"], obj.link)
        self.assertEqual(
            results["imageUrl"], "http://testserver/media/" + str(obj.imageUrl)
        )

    def test_places_info_field_context(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)

        PlaceFactory.create_batch(3)
        obj_non_gender = Place.objects.get(id=1)
        obj_non_gender.gender = None
        obj_non_gender.save()

        obj = Place.objects.get(id=3)
        response = client.get(ViewPlacesTests.path_places).data
        results = response["results"]
        self.assertEqual(
            results[0]["info"],
            "{} лет. {} отдых".format(
                str(obj_non_gender.age),
                obj_non_gender.get_activity_type(obj_non_gender.activity_type),
            ),
        )
        self.assertEqual(
            results[2]["info"],
            "{}, {} лет. {} отдых".format(
                obj.get_gender(obj.gender),
                str(obj.age),
                obj.get_activity_type(obj.activity_type),
            ),
        )

    def test_places_tag_field_correct(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)
        tag = PlacesTagFactory(name="test", slug="test")
        PlaceFactory.create_batch(1)
        obj = Place.objects.get(pk=1)
        obj.tags.add(tag)
        obj.save()
        response = client.get(ViewPlacesTests.path_places).data
        results = response["results"][0]["tags"][0]["name"]
        self.assertTrue(str(tag) in results)

    def test_places_post_unauthorized_client(self):
        client = ViewPlacesTests.unauthorized_client
        place = {
            "activity_type": 1,
            "chosen": False,
            "title": "123",
            "address": "1234",
            "city": ViewPlacesTests.city.id,
            "description": "1235",
        }
        response = client.post(
            path=ViewPlacesTests.path_places,
            data=place,
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_places_post_authorized_client(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)
        tag = PlacesTagFactory(name="test", slug="test")
        place = {
            "age": 10,
            "activity_type": 1,
            "title": "123",
            "address": "1234",
            "city": ViewPlacesTests.city.id,
            "description": "1235",
            "tags": {tag.slug},
        }
        response = client.post(
            path=ViewPlacesTests.path_places,
            data=place,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            201,
            msg="Проверьте отправленные данные, не все поля заполнены",
        )

    def test_places_post_empty_data(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)
        response = client.post(
            path=ViewPlacesTests.path_places,
        )
        self.assertEqual(response.status_code, 400)
