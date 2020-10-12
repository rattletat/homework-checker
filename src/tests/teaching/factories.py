import factory
from apps.teaching.models import Lecture, Lesson


class LectureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lecture

    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("paragraph", nb_sentences=10)


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson

    lecture = factory.SubFactory(LectureFactory)

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=5)
