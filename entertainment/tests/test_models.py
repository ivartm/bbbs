from django.core.exceptions import ValidationError
from django.test import TestCase

from entertainment.factories import ArticleFactory
from entertainment.models import Article


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
            article_test.clean()

    def test_article_save(self):
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
