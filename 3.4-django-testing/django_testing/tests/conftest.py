from datetime import datetime

import pytest
from model_bakery import baker
from rest_framework.test import APIClient


from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_f():
    return Student.objects.create(name="Тест-студент", birth_date=datetime.now())


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_f():
    return Course.objects.create(name="Тест-курс")


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory
