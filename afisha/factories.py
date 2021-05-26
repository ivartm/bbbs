from datetime import timedelta
import factory
import pytz
from faker import Faker

from common.models import City
from afisha.models import Event, EventParticipant

from users.factories import UserFactory

fake = Faker(["ru-RU"])


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
        end_date=factory.LazyAttribute(
            lambda obj: obj.start_date + timedelta(days=60)
        ),
        tzinfo=pytz.UTC,
    )
    seats = factory.Faker("random_int", min=0, max=50)
    city = factory.Iterator(City.objects.all())


class EventParticipantFactory(factory.django.DjangoModelFactory):
    """This factory create itself User and Profile fixtures."""
    class Meta:
        model = EventParticipant
        django_get_or_create = [
            "user",
            "event",
        ]

    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventFactory)
