from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Lecture


def home_view(request):
    return render(request, "pages/home.html", context={})


class LectureList(ListView):
    template_name = "lectures/index.html"
    model = Lecture


class LectureDetail(DetailView):
    template_name = "lectures/detail.html"
    model = Lecture


class LessonList(ListView):
    template_name = "lectures/index.html"
    model = Lecture


class LessonDetail(DetailView):
    template_name = "lectures/detail.html"
    model = Lecture
