import factory
from django.contrib.auth import get_user_model
from django.db.models import F, signals
from faker import Faker

from afisha.models import Event, EventParticipant
from common.models import City
from users.models import Profile

User = get_user_model()
fake = Faker(["ru-RU"])


@factory.django.mute_signals(signals.post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    """Creates profile itself or could be called as RelatedFactory.

    Rely on City objects, be sure at least one city is present.
    Please review factory_boy docs why "mute_signals" decorator is
    required here.
    """

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
        django_get_or_create = ["username"]

    username = factory.Sequence(lambda n: "user_%d" % (User.objects.count()))
    password = "Bbbs2021!"
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@bbbs.com")
    profile = factory.RelatedFactory(
        ProfileFactory, factory_related_name="user"
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call.

        The method has been taken from factory_boy manual. Without it
        password for users is being created without HASH and doesn't work
        right.
        """

        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)

    @factory.post_generation
    def num_events(self, create, extracted, **kwargs):
        """Keyword argument to book user on events during factory creation.

        Assumes there are enough Event objects in users's city in DB. Counts
        the events and select what is less: available events or "extracted"
        argument. Creates EventParticipant object.
        """

        if not create:
            return

        if extracted is None:
            return

        user_afisha = Event.afisha_objects.user_afisha(user=self)
        not_booked_events = user_afisha.filter(booked=False)
        events_with_seat = not_booked_events.filter(takenSeats__lt=F("seats"))

        events_count = events_with_seat.count()
        how_many = min(events_count, extracted)

        events_to_book = events_with_seat.order_by("?")[:how_many]

        for event in events_to_book:
            EventParticipant.objects.create(user=self, event=event)
