from django.test import TestCase

# from rights.factories import RightFactory, RightTagFactory
from rights.models import RightTag


class RightTagModelTest(TestCase):
    def test_righttag_has_slug(self):
        """RightTag without tag make it itself."""
        tag = RightTag.objects.create(name="Some tag")
        assert (
            tag.slug
        ), "Убедитесь что в словаре для тегов генерируется 'slug'."

    def test_righttag_uses_given_slug(self):
        """Righttag with given slug doesn't override it itself."""
        expected_slug = "something-different"
        tag = RightTag.objects.create(name="Some Name", slug=expected_slug)
        self.assertEqual(
            tag.slug,
            expected_slug,
            msg="Убедитесь, что заданный slug при создании не меняется.",
        )

    def test_righttag_slug_is_ascii(self):
        """Cyrillic name should have ASCII slug in right manner."""
        tag = RightTag.objects.create(name="Фильдиперсовая рубаха ЙАРРР!")
        self.assertTrue(
            tag.slug.isascii(),
            msg=(
                f"Убедитесь, что 'slug' содержит только ASCII символы."
                f"Полученное значение slug: {tag.slug}"
            ),
        )
        self.assertEqual(
            tag.slug,
            "fildipersovaya-rubakha-jarrr",
            msg="Убедитесь, что транслитерация кириллицы без ошибок",
        )


# class RightModelTest(TestCase):
#     @classmethod
#     def setUp(self):
#         self.tag = RightTagFactory()
#         self.right = RightFactory()

#     def test_right_has_colored_circle_property(self):
#         """Right obj has to have 'colored_circle' property."""
#         right = self.right
#         assert (
#             right.colored_circle
#         ), "Убедитесь что у объекта есть свойство 'colored_circle'."

#     def test_right_circle_propert_html(self):
#         """Be sure 'colored_circle' property returns right html."""
#         self.right.color = "Light Blue"
#         expected_html = (
#             "<span style='"
#             "height: 25px;"
#             "width: 25px;"
#             "border: 1px solid grey;"
#             "border-radius: 50%;"
#             "display: inline-block;"
#             "background-color: Light Blue;'>"
#             "</span>"
#         )
#         self.assertHTMLEqual(
#             self.right.colored_circle,
#             expected_html,
#             msg="Убедитесь, что 'colored_circle' отдает ожидаемый html.",
#         )
