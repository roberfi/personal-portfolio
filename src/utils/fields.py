from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models

if TYPE_CHECKING:
    from django.db.backends.base.base import BaseDatabaseWrapper
    from django.db.models.expressions import Expression


class EncryptedJSONField(models.TextField[dict[str, Any], dict[str, Any]]):
    """A TextField that transparently stores a dict as Fernet-encrypted JSON.

    Not a JSONField subclass: the encrypted value is ciphertext, not valid JSON,
    which doesn't play well with native jsonb columns and their adapters.
    """

    def from_db_value(
        self, value: str | None, expression: Expression, connection: BaseDatabaseWrapper
    ) -> dict[str, Any] | None:
        if value is None:
            return None
        decrypted = Fernet(settings.FIELD_ENCRYPTION_KEY.encode()).decrypt(value.encode())
        return json.loads(decrypted.decode())  # type: ignore[no-any-return]

    def to_python(self, value: Any) -> dict[str, Any] | None:
        if value is None or isinstance(value, dict):
            return value
        decrypted = Fernet(settings.FIELD_ENCRYPTION_KEY.encode()).decrypt(value.encode())
        return json.loads(decrypted.decode())  # type: ignore[no-any-return]

    def get_prep_value(self, value: Any) -> str | None:
        if value is None:
            return None
        encrypted = Fernet(settings.FIELD_ENCRYPTION_KEY.encode()).encrypt(json.dumps(value).encode())
        return encrypted.decode()
