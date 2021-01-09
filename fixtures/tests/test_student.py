import pytest
from datetime import datetime

from fixtures.app.student import Student


# Can specify scope="function"/"module" etc
@pytest.fixture()
def dummy_student():
    return Student("John", datetime(2000, 1, 1), "CSE")


def test_get_age(dummy_student):
    age = (datetime.now() - dummy_student.dob).days
    assert dummy_student.get_age() == age


def test_add_credits(dummy_student):
    dummy_student.add_credits(5)
    assert dummy_student.get_credits() == 5


def test_get_credits(dummy_student):
    assert dummy_student.get_credits() == 0
