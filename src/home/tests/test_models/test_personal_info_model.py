from __future__ import annotations

from typing import ClassVar

from django.test import TestCase

from home.models import PersonalInfo


class TestPersonalInfoModel(TestCase):
    personal_info: ClassVar[PersonalInfo]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.personal_info = PersonalInfo(name="Test Name", description="Test description", biography="That's me")

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.personal_info),
            expected_str := self.personal_info.name,
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )
