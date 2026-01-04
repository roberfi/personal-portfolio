from __future__ import annotations

from typing import ClassVar

from django.test import TestCase

from home.models import PersonalInfo, Technology

# Constants
TEST_NAME = "Test Name"
TEST_DESCRIPTION = "Test description"
TEST_INTRODUCTION = "That's me"
TEST_BIOGRAPHY = "That's my biography"


class TestPersonalInfoModel(TestCase):
    personal_info: ClassVar[PersonalInfo]
    tech1: ClassVar[Technology]
    tech2: ClassVar[Technology]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.personal_info = PersonalInfo.objects.create(
            name=TEST_NAME, title=TEST_DESCRIPTION, introduction=TEST_INTRODUCTION, biography=TEST_BIOGRAPHY
        )
        cls.tech1 = cls.personal_info.technologies.create(name="Tech 1", priority=2)
        cls.tech2 = cls.personal_info.technologies.create(name="Tech 2", priority=1)

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.personal_info),
            expected_str := self.personal_info.name,
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )

    def test_technologies_ordering(self) -> None:
        ordered_technologies = list(self.personal_info.technologies.all())
        self.assertEqual(
            ordered_technologies,
            [self.tech2, self.tech1],
            "The technologies are not ordered by priority as expected",
        )
