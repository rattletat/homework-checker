import factory
from django.conf import settings
from django.contrib.auth import get_user_model


from apps.accounts.models import Student


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall(
        "set_password", get_user_model().objects.make_random_password()
    )
    full_name = factory.Faker("name")
    is_active = True
    is_student = False


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory, is_student=True)
    identifier = factory.Faker("random_number", digits=6, fix_len=True)
