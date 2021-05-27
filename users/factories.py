import factory
from django.contrib.auth import get_user_model
from django.db.models import signals
from faker import Faker

from common.models import City
from users.models import Profile

User = get_user_model()
fake = Faker(["ru-RU"])


@factory.django.mute_signals(signals.post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    """Please review factory_boy docs why decoratory is required here."""

    class Meta:
        model = Profile
        django_get_or_create = ["user"]

    city = factory.Iterator(City.objects.all())
    user = factory.SubFactory("users.factories.UserFactory", profile=None)
    role = factory.Iterator(Profile.Role.choices, getter=lambda role: role[0])


@factory.django.mute_signals(signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):
    """Please review factory_boy docs why decoratory is required here."""

    class Meta:
        model = User
        django_get_or_create = [
            "username",
        ]

    username = factory.Sequence(lambda n: "user_%d" % n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@bbbs.com")
    profile = factory.RelatedFactory(
        ProfileFactory, factory_related_name="user"
    )
