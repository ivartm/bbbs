from django.contrib.auth import get_user_model
import factory

from django.db.models import signals
import pytz

from .models import Event, EventParticipant
from common.models import City
from users.models import Profile

from faker import Faker


User = get_user_model()
fake = Faker(["ru-RU"])


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
        django_get_or_create = [
            "name",
        ]

    name = factory.Faker("city", locale="ru-RU")
    is_primary = factory.Faker("boolean", chance_of_getting_true=10)


@factory.django.mute_signals(signals.post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    """Please review factory_boy docs why decoratory is required here."""

    class Meta:
        model = Profile
        django_get_or_create = ["user"]

    city = factory.SubFactory(CityFactory)
    user = factory.SubFactory("afisha.factories.UserFactory", profile=None)
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


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    address = factory.Faker("address")
    contact = factory.LazyAttribute(
        lambda x: f"{fake.name()}, {fake.phone_number()}"
    )
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")
    start_at = factory.Faker(
        "date_time_this_year",
        before_now=True,
        after_now=True,
        tzinfo=pytz.UTC,
    )
    end_at = factory.Faker(
        "date_time_between",
        start_date=factory.SelfAttribute("..start_at"),
        end_date="+1m",
        tzinfo=pytz.UTC,
    )
    seats = factory.Faker("random_int", min=0, max=50)
    city = factory.SubFactory(CityFactory)


@factory.django.mute_signals(signals.post_save)
class EventParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventParticipant
        django_get_or_create = [
            "user",
            "event",
        ]

    user = factory.SubFactory("afisha.factories.UserFactory", profile=None)
    event = factory.SubFactory(EventFactory)
