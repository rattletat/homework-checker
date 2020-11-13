def get_lecture_rsc_path(obj, filename):
    return f"lectures/{obj.lecture.slug}/rsc/{filename}"


def get_lesson_rsc_path(obj, filename):
    return f"lectures/{obj.lesson.lecture.slug}/lessons/{obj.lesson.slug}/rsc/{filename}"
