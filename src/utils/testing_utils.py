from __future__ import annotations

from datetime import date
from typing import Self


def get_date_with_mocked_today(year: int, month: int, day: int) -> type[date]:
    class MockedDate(date):
        @classmethod
        def today(cls) -> Self:
            return cls(year, month, day)

    return MockedDate
