import datetime
import random

import factory
from apps.homework.models import Exercise, Submission
from tests.accounts.factories import UserFactory
from tests.teaching.factories import LessonFactory


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    lesson = factory.SubFactory(LessonFactory)
    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("paragraph", nb_sentences=10)
    max_score = random.randrange(1, 50)


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Submission

    exercise = factory.SubFactory(ExerciseFactory)
    user = factory.SubFactory(UserFactory)
    score = factory.LazyAttribute(
        lambda submission: random.randrange(1, submission.exercise.max_score)
    )
    output = factory.Faker("paragraph", nb_sentences=10)
