from django.core.exceptions import ValidationError
from django.test import TestCase

from bbbs.entertainment.factories import ArticleFactory
from bbbs.entertainment.models import Article


class ArticleModelTest(TestCase):
    def test_article_clean(self):
        ArticleFactory.create_batch(10)
        article_main = Article.objects.get(id=1)
        article_test = Article.objects.get(id=2)

        article_main.is_main = True
        article_main.save()

        article_test.is_main = True
        with self.assertRaises(
            ValidationError, msg="Основная статья может быть только одна!"
        ):
            article_test.full_clean()

    def test_article_save(self):

        """
        Test save method for opportunity to change is_main flag in False
            if it set by another article
        """

        ArticleFactory.create_batch(10)
        article_main = Article.objects.get(id=1)
        article_main.is_main = True
        article_main.save()
        article_test = Article.objects.get(id=2)
        article_test.is_main = True
        article_test.save()
        self.assertEqual(article_main.is_main, True)
        self.assertEqual(
            article_test.is_main,
            False,
            msg="Если уже есть основная, нельзя установить еще одну",
        )

    def test_a_article_save_twice(self):

        """Test save method for impossibility to change is_main flag"""

        ArticleFactory.create_batch(10)
        article_main = Article.objects.get(id=1)
        article_main.is_main = True
        article_main.save()
        self.assertEqual(article_main.is_main, True)
        article_main.save()
        self.assertEqual(article_main.is_main, True)


#  на будущее
# class MovieModelTest(TestCase):
#     def test_movie_clean(self):
#
#         MovieTagFactory.create_batch(10)
#         tag = MovieTag.objects.get(id=1)
#
#         movie = Movie.objects.create(link="https://rutube.ru")
#         movie.tags.add(tag)
#         movie.save()
#         with self.assertRaises(
#             ValidationError, msg="Можно добавить только с youtube"
#         ):
#             movie.full_clean()
