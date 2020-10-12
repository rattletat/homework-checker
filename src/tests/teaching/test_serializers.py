# import pytest
# from apps.api.serializers import LectureSerializer, LessonSerializer

# from .factories import LectureFactory


def validate_serializer(serializer, data, errors={}, valid=True):
    assert valid == serializer.is_valid()
    assert serializer.data == data
    assert serializer.validated_data == (data if valid else {})
    assert serializer.errors == ({} if valid else errors)


# class TestLectureSerializer:
#     @pytest.mark.django_db
#     def test_valid_data(self):
#         lecture = LectureFactory()
#         valid_data = {"title": lecture.title}
#         serializer = LectureSerializer(data=valid_data)

#         validate_serializer(serializer, valid_data, valid=True)

# def test_invalid_blank_field(self):
#     invalid_data = {"title": ""}
#     errors = {"title": ["This field may not be blank."]}
#     serializer = LectureSerializer(data=invalid_data)

#     validate_serializer(serializer, invalid_data, errors=errors, valid=False)

# def test_invalid_missing_field(self):
#     invalid_data = {}
#     errors = {"title": ["This field is required."]}
#     serializer = LectureSerializer(data=invalid_data)

#     validate_serializer(serializer, invalid_data, errors=errors, valid=False)


# class TestLessonSerializer:
#     def test_valid_data(self):
#         valid_data = {"title": "Lesson 101"}
#         serializer = LessonSerializer(data=valid_data)

#         validate_serializer(serializer, valid_data, valid=True)

#     def test_invalid_blank_field(self):
#         invalid_data = {"title": ""}
#         errors = {"title": ["This field may not be blank."]}
#         serializer = LessonSerializer(data=invalid_data)

#         validate_serializer(serializer, invalid_data, errors=errors, valid=False)

#     def test_invalid_missing_field(self):
#         invalid_data = {}
#         errors = {"title": ["This field is required."]}
#         serializer = LessonSerializer(data=invalid_data)

#         validate_serializer(serializer, invalid_data, errors=errors, valid=False)
