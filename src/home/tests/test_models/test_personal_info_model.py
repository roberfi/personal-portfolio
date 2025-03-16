from __future__ import annotations

from typing import ClassVar

from django.test import TestCase

from home.models import PersonalInfo

# Constants
TEST_NAME = "Test Name"
TEST_DESCRIPTION = "Test description"
TEST_BIOGRAPHY = "That's me"


class TestPersonalInfoModel(TestCase):
    personal_info: ClassVar[PersonalInfo]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.personal_info = PersonalInfo(name=TEST_NAME, description=TEST_DESCRIPTION, biography=TEST_BIOGRAPHY)

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.personal_info),
            expected_str := self.personal_info.name,
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )
