from __future__ import annotations

from datetime import date
from typing import Self


def get_date_with_mocked_today(today_date: date) -> type[date]:
    class MockedDate(date):
        @classmethod
        def today(cls) -> Self:
            return cls(today_date.year, today_date.month, today_date.day)

    return MockedDate
