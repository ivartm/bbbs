from datetime import timedelta

import factory
import pytz
from faker import Faker

from bbbs.afisha.models import Event, EventParticipant
from bbbs.common.models import City
from bbbs.users.factories import UserFactory

fake = Faker(["ru-RU"])


class EventFactory(factory.django.DjangoModelFactory):
    """Rely on City objects. They should be in DB prior run."""

    class Meta:
        model = Event

    address = factory.Faker("address")
    contact = factory.LazyAttribute(
        lambda x: f"{fake.name()}, {fake.phone_number()}"
    )
    title = factory.Sequence(lambda t: f"{fake.sentence(nb_words=3)} {t}")
    description = factory.Faker("text")
    start_at = factory.Faker(
        "date_time_this_year",
        before_now=False,
        after_now=True,
        tzinfo=pytz.UTC,
    )
    end_at = factory.Faker(
        "date_time_between",
        start_date=factory.SelfAttribute("..start_at"),
        end_date=factory.LazyAttribute(
            lambda obj: obj.start_date + timedelta(hours=48)
        ),
        tzinfo=pytz.UTC,
    )
    seats = factory.Faker("random_int", min=0, max=50)
    city = factory.Iterator(City.objects.all())


class EventParticipantFactory(factory.django.DjangoModelFactory):
    """Creates User and Profile objects itself."""

    class Meta:
        model = EventParticipant
        django_get_or_create = [
            "user",
            "event",
        ]

    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventFactory)
