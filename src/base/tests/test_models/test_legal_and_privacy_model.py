from __future__ import annotations

from typing import ClassVar

from django.test import TestCase

from base.models import LegalAndPrivacy


class TestLegalAndPrivacyModel(TestCase):
    legal_and_privacy: ClassVar[LegalAndPrivacy]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.legal_and_privacy = LegalAndPrivacy(id=1, title="Legal text", text="Privacy text")

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.legal_and_privacy),
            expected_str := self.legal_and_privacy.title,
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )

    def test_model_name(self) -> None:
        self.assertEqual(
            returned_name := self.legal_and_privacy.modal_name,
            expected_name := "legal_and_privacy_modal_1",
            f"The modal_name property is returning '{returned_name}' instead the expected value '{expected_name}'",
        )
