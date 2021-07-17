from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from bbbs.entertainment.factories import (
    ArticleFactory,
    BookFactory,
    BookTagFactory,
    GuideFactory,
    MovieTagFactory,
    VideoTagFactory,
)
from bbbs.entertainment.models import Movie, Video


class EntertainmentTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.paths = {
            "guide": reverse("guides-list"),
            "movie": reverse("movies-list"),
            "video": reverse("videos-list"),
            "book": reverse("books-list"),
            "article": reverse("articles-list"),
            "video_tags": reverse("videos-tags-list"),
            "movie_tags": reverse("movies-tags-list"),
            "book_tags": reverse("books-tags-list"),
        }
        BookTagFactory.create_batch(2)
        MovieTagFactory.create_batch(2)
        VideoTagFactory.create_batch(2)
        BookFactory.create_batch(2)
        ArticleFactory.create_batch(2)
        GuideFactory.create_batch(2)
        Movie.objects.create(
            title="test",
            description="test",
            producer="prod",
            year=1994,
            link="https://rutube.ru",
        )
        Video.objects.create(
            title="test", author="prod", link="https://rutube.ru"
        )

    def test_entertainemt_get_list_url(self):
        client = APIClient()
        for path in self.paths.values():
            with self.subTest(path=path):
                response = client.get(path)
                self.assertEqual(
                    response.status_code, 200, msg=f"Проверьте путь {path}"
                )

    def test_entertainemt_get_detail_url(self):
        client = APIClient()
        for path in self.paths.values():
            with self.subTest(path=path):
                response = client.get(path + "1/")
                if "tags" in path:
                    self.assertEqual(
                        response.status_code,
                        404,
                        msg=f"Проверьте путь {path}1/",
                    )
                else:
                    self.assertEqual(
                        response.status_code,
                        200,
                        msg=f"Проверьте путь {path}1/",
                    )

    def test_entertainemt_allow_methods_list(self):
        client = APIClient()
        for path in self.paths.values():
            with self.subTest(path=path):
                response = client.put(path)
                self.assertEqual(
                    response.status_code, 405, msg=f"Проверьте путь {path}"
                )

                response = client.patch(path)
                self.assertEqual(
                    response.status_code, 405, msg=f"Проверьте путь {path}"
                )

                response = client.post(path)
                self.assertEqual(
                    response.status_code, 405, msg=f"Проверьте путь {path}"
                )

                response = client.delete(path)
                self.assertEqual(
                    response.status_code, 405, msg=f"Проверьте путь {path}"
                )

    def test_entertainemt_allow_methods_detail(self):
        client = APIClient()
        for path in self.paths.values():
            with self.subTest(path=path):
                response = client.put(path + "1/")
                if "tags" in path:
                    self.assertEqual(
                        response.status_code,
                        404,
                        msg=f"Проверьте путь {path}1/",
                    )
                else:
                    self.assertEqual(
                        response.status_code,
                        405,
                        msg=f"Проверьте путь {path}1/",
                    )

                response = client.patch(path + "1/")
                if "tags" in path:
                    self.assertEqual(
                        response.status_code,
                        404,
                        msg=f"Проверьте путь {path}1/",
                    )
                else:
                    self.assertEqual(
                        response.status_code,
                        405,
                        msg=f"Проверьте путь {path}1/",
                    )

                response = client.post(path + "1/")
                if "tags" in path:
                    self.assertEqual(
                        response.status_code,
                        404,
                        msg=f"Проверьте путь {path}1/",
                    )
                else:
                    self.assertEqual(
                        response.status_code,
                        405,
                        msg=f"Проверьте путь {path}1/",
                    )

                response = client.delete(path + "1/")
                if "tags" in path:
                    self.assertEqual(
                        response.status_code,
                        404,
                        msg=f"Проверьте путь {path}1/",
                    )
                else:
                    self.assertEqual(
                        response.status_code,
                        405,
                        msg=f"Проверьте путь {path}1/",
                    )
