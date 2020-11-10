def get_lecture_rsc_path(obj, filename):
    return f"lectures/{obj.entity.slug}/rsc/{filename}"


def get_lesson_rsc_path(obj, filename):
    return f"lectures/{obj.entity.lecture.slug}/lessons/{obj.entity.slug}/rsc/{filename}"
