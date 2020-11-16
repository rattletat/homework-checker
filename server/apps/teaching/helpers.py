def get_lecture_rsc_path(resource, filename):
    lecture_slug = resource.lecture.slug
    return f"lectures/{lecture_slug}/rsc/{filename}"


def get_lesson_rsc_path(resource, filename):
    lecture_slug = resource.lesson.lecture.slug
    lesson_slug = resource.lesson.slug
    return f"lectures/{lecture_slug}/lessons/{lesson_slug}/rsc/{filename}"
