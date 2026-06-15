from __future__ import annotations

import json

from django.test import TestCase

from utils.fields import EncryptedJSONField


class TestEncryptedJSONField(TestCase):
    """Test cases for EncryptedJSONField."""

    def setUp(self) -> None:
        self.field = EncryptedJSONField()

    def test_round_trip(self) -> None:
        """Test that a dict survives encryption and decryption unchanged."""
        data = {"host": "smtp.example.com", "port": 587, "api_key": "super-secret"}

        encrypted = self.field.get_prep_value(data)

        self.assertIsNotNone(encrypted, "get_prep_value() should not return None for a non-None dict")
        self.assertEqual(
            decrypted := self.field.to_python(encrypted),
            data,
            f"to_python(get_prep_value(data)) returned '{decrypted}' instead of the original '{data}'",
        )

    def test_value_is_encrypted_at_rest(self) -> None:
        """Test that the stored value is ciphertext, not the plaintext JSON."""
        data = {"api_key": "super-secret"}

        encrypted = self.field.get_prep_value(data)

        assert encrypted is not None
        self.assertNotIn(
            "super-secret", encrypted, f"The encrypted value '{encrypted}' should not contain the plaintext secret"
        )
        self.assertNotEqual(
            encrypted,
            json.dumps(data),
            f"The encrypted value '{encrypted}' should not equal the plaintext JSON representation",
        )

    def test_none_round_trip(self) -> None:
        """Test that None is preserved by get_prep_value and to_python."""
        self.assertIsNone(
            prepped := self.field.get_prep_value(None), f"get_prep_value(None) returned '{prepped}' instead of None"
        )
        self.assertIsNone(parsed := self.field.to_python(None), f"to_python(None) returned '{parsed}' instead of None")
