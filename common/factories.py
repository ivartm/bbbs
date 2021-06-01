import factory

from common.models import City


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
        django_get_or_create = [
            "name",
        ]

    name = factory.Faker("city")
    timeZone = factory.Iterator(City.TIMEZONE_CHOICES, getter=lambda tz: tz[0])
    isPrimary = factory.Faker(
        "boolean",
        chance_of_getting_true=20,
    )
