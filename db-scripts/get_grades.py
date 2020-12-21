from django.contrib.auth import get_user_model
from apps.teaching.models import Lecture

User = get_user_model()

lec1 = Lecture.objects.first()
lec2 = Lecture.objects.last()

for u in lec2.participants.all():
    full_name = u.full_name
    identifier = u.identifier
    score = lecture.get_score(u)
    grade = lecture.grading_scale.get_grade(score)

    print(score, grade, identifier, full_name, sep="\t")


# Doing all the same
qs1 = User.objects.filter(enrolled_lectures__in=[lec2])
qs2 = User.objects.filter(enrolled_lectures=lec2)
qs3 = lec2.participants.all()

