def get_lecture_rsc_path(resource, filename):
    lecture_id = resource.lecture.id
    return f"lectures/{lecture_id}/rsc/{filename}"


def get_lesson_rsc_path(resource, filename):
    lecture_id = resource.lesson.lecture.id
    lesson_id = resource.lesson.id
    return f"lectures/{lecture_id}/lessons/{lesson_id}/rsc/{filename}"
