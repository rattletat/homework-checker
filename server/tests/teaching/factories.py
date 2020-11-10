from datetime import timedelta

import factory
from apps.teaching.models import Lecture, Lesson
from django.utils.timezone import now


class LectureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lecture

    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("paragraph", nb_sentences=10)
    start = now() - timedelta(days=30)
    end = now() + timedelta(days=30)


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson

    lecture = factory.SubFactory(LectureFactory)

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=5)
