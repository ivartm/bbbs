from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from entertainment.factories import ArticleFactory
from entertainment.models import Article, Book, BookTag


class ViewArticlesTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.path_articles = reverse("articles-list")

    def test_articles_list_correct_fields(self):
        client = APIClient()
        ArticleFactory.create_batch(10)
        response = client.get(ViewArticlesTests.path_articles).data
        self.assertTrue("count" in response)
        self.assertTrue("next" in response)
        self.assertTrue("previous" in response)
        self.assertTrue("results" in response)

        fields = [
            "id",
            "is_main",
            "title",
            "author",
            "profession",
            "text",
            "color",
            "image_url",
        ]
        results = response.get("results")[0]
        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in results, msg=f"Нет поля {field}")

    def test_articles_list_context(self):
        client = APIClient()
        ArticleFactory.create_batch(10)
        response = client.get(ViewArticlesTests.path_articles).data
        self.assertEqual(response["count"], 10)

        results = response.get("results")[0]
        obj = Article.objects.get(pk=1)

        self.assertEqual(results["id"], obj.pk)
        self.assertEqual(results["is_main"], obj.is_main)
        self.assertEqual(results["title"], obj.title)
        self.assertEqual(results["author"], obj.author)
        self.assertEqual(results["profession"], obj.profession)
        self.assertEqual(results["text"], obj.text)
        self.assertEqual(results["color"], obj.color)
        self.assertEqual(
            results["image_url"],
            "http://testserver/media/" + str(obj.image_url),
        )

    def test_article_detail_fields(self):
        client = APIClient()
        ArticleFactory.create_batch(10)
        response = client.get(ViewArticlesTests.path_articles + "1/").data
        fields = [
            "id",
            "is_main",
            "title",
            "author",
            "profession",
            "text",
            "color",
            "image_url",
        ]

        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in response, msg=f"Нет поля {field}")

    def test_article_detail_context(self):
        client = APIClient()
        ArticleFactory.create_batch(10)
        response = client.get(ViewArticlesTests.path_articles + "1/").data

        obj = Article.objects.get(pk=1)

        self.assertEqual(response["id"], obj.pk)
        self.assertEqual(response["is_main"], obj.is_main)
        self.assertEqual(response["title"], obj.title)
        self.assertEqual(response["author"], obj.author)
        self.assertEqual(response["profession"], obj.profession)
        self.assertEqual(response["text"], obj.text)
        self.assertEqual(response["color"], obj.color)
        self.assertEqual(
            response["image_url"],
            "http://testserver/media/" + str(obj.image_url),
        )

    def test_articles_allowed_methods(self):
        client = APIClient()

        response = client.get(ViewArticlesTests.path_articles)
        self.assertEqual(
            response.status_code, 200, msg="Метод GET должен быть доступен!"
        )

        response = client.post(ViewArticlesTests.path_articles)
        self.assertEqual(
            response.status_code, 405, msg="Метод POST должен быть недоступен!"
        )

        response = client.patch(ViewArticlesTests.path_articles)
        self.assertEqual(
            response.status_code,
            405,
            msg="Метод PATCH должен быть недоступен!",
        )

        response = client.put(ViewArticlesTests.path_articles)
        self.assertEqual(
            response.status_code, 405, msg="Метод PUT должен быть недоступен!"
        )

        response = client.delete(ViewArticlesTests.path_articles)
        self.assertEqual(
            response.status_code,
            405,
            msg="Метод DELETE должен быть недоступен!",
        )


class ViewBookTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.path_books = reverse("books-list")

    def test_books_correct_fields(self):
        client = APIClient()
        tag = BookTag.objects.create(name="test", slug="test", color="#FF0000")
        Book.objects.create(
            tag=tag,
            title="book",
            author="ya",
            year=1990,
            description="blablaba",
            link="ya.ru",
        )

        response = client.get(ViewBookTests.path_books).data
        self.assertTrue("count" in response)
        self.assertTrue("next" in response)
        self.assertTrue("previous" in response)
        self.assertTrue("results" in response)

        fields = [
            "id",
            "tag",
            "title",
            "author",
            "year",
            "description",
            "color",
            "link",
        ]
        results = response.get("results")[0]
        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in results, msg=f"Нет поля {field}")

    def test_books_list_context(self):
        client = APIClient()
        tag = BookTag.objects.create(name="test", slug="test", color="#FF0000")
        obj = Book.objects.create(
            tag=tag,
            title="book",
            author="ya",
            year=1990,
            description="blablaba",
            link="ya.ru",
        )

        response = client.get(ViewBookTests.path_books).data
        self.assertEqual(response["count"], 1)
        results = response.get("results")[0]

        self.assertEqual(results["id"], obj.pk)
        self.assertEqual(results["tag"]["slug"], tag.slug)
        self.assertEqual(results["title"], obj.title)
        self.assertEqual(results["author"], obj.author)
        self.assertEqual(results["year"], obj.year)
        self.assertEqual(results["description"], obj.description)
        self.assertEqual(results["color"], tag.color)
        self.assertEqual(results["link"], obj.link)

    def test_books_allowed_methods(self):
        client = APIClient()

        response = client.get(ViewBookTests.path_books)
        self.assertEqual(
            response.status_code, 200, msg="Метод GET должен быть доступен!"
        )

        response = client.post(ViewBookTests.path_books)
        self.assertEqual(
            response.status_code, 405, msg="Метод POST должен быть недоступен!"
        )

        response = client.patch(ViewBookTests.path_books)
        self.assertEqual(
            response.status_code,
            405,
            msg="Метод PATCH должен быть недоступен!",
        )

        response = client.put(ViewBookTests.path_books)
        self.assertEqual(
            response.status_code, 405, msg="Метод PUT должен быть недоступен!"
        )

        response = client.delete(ViewBookTests.path_books)
        self.assertEqual(
            response.status_code,
            405,
            msg="Метод DELETE должен быть недоступен!",
        )
