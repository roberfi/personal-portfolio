from __future__ import annotations

from typing import ClassVar

from django.test import TestCase

from home.models import Technology

TEST_NAME_1 = "Django"
TEST_NAME_2 = "Python"
TEST_NAME_3 = "Tailwind"


class BaseTestTechnologyModel(TestCase):
    @staticmethod
    def _make(name: str, priority: int = 0) -> Technology:
        return Technology.objects.create(name=name, priority=priority)


class TestTechnologyModel(BaseTestTechnologyModel):
    technology: ClassVar[Technology]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.technology = cls._make(TEST_NAME_1)

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.technology),
            TEST_NAME_1,
            f"The __str__ method is returning '{returned_str}' instead of the expected '{TEST_NAME_1}'",
        )

    def test_default_priority_is_zero(self) -> None:
        self.assertEqual(
            self.technology.priority,
            0,
            f"Technology 'priority' field should default to 0, got {self.technology.priority}",
        )


class TestTechnologyOrdering(BaseTestTechnologyModel):
    tech_a: ClassVar[Technology]
    tech_b: ClassVar[Technology]
    tech_c: ClassVar[Technology]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.tech_a = cls._make(TEST_NAME_3, priority=2)
        cls.tech_b = cls._make(TEST_NAME_1, priority=1)
        cls.tech_c = cls._make(TEST_NAME_2, priority=1)

    def test_ordered_by_priority_then_name(self) -> None:
        techs = list(Technology.objects.filter(name__in=(TEST_NAME_1, TEST_NAME_2, TEST_NAME_3)))

        self.assertEqual(
            techs[0],
            self.tech_b,
            f"First technology should be '{TEST_NAME_1}' (priority=1), got '{techs[0].name}'",
        )
        self.assertEqual(
            techs[1],
            self.tech_c,
            f"Second technology should be '{TEST_NAME_2}' (priority=1, after Django alphabetically),"
            f" got '{techs[1].name}'",
        )
        self.assertEqual(
            techs[2],
            self.tech_a,
            f"Third technology should be '{TEST_NAME_3}' (priority=2), got '{techs[2].name}'",
        )
