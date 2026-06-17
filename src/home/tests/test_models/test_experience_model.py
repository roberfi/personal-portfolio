from __future__ import annotations

from datetime import date
from typing import ClassVar
from unittest.mock import patch

from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ValidationError
from django.test import TestCase

from home.models import DatedModel, Experience, Technology
from utils.test_utils.mocks import get_date_with_mocked_today

# Constants
TEST_TITLE = "Test Title"
TEST_LOCATION = "Any Location"
TEST_COMPANY = "Any Company"
TEST_DESCRIPTION = "Description of the experience"
DEFAULT_START_DATE = date(2012, 10, 25)

MOCKED_TODAY_DATE = date(2017, 9, 15)


class BaseTestExperienceModel(TestCase):
    experience: ClassVar[Experience]

    @staticmethod
    def _get_new_experience_instance(
        *, company: str = TEST_COMPANY, start_date: date = DEFAULT_START_DATE, end_date: date | None = None
    ) -> Experience:
        return Experience.objects.create(
            title=TEST_TITLE,
            location=TEST_LOCATION,
            institution=company,
            description=TEST_DESCRIPTION,
            start_date=start_date,
            end_date=end_date,
        )

    def _assert_actual_end_date_value(self, model: DatedModel, expected_date: date) -> None:
        self.assertEqual(
            actual_end_date := model.actual_end_date,
            expected_date,
            f"The returned actual end date is '{actual_end_date}' instead of the expected '{expected_date}'",
        )

    def _assert_duration_value(self, model: DatedModel, expected_duration: str) -> None:
        self.assertEqual(
            returned_duration := model.duration,
            expected_duration,
            f"The returned duration is '{returned_duration}' instead of the expected '{expected_duration}'",
        )


class TestExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2015, 8, 29))

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.experience),
            expected_str := f"{self.experience.title} at {self.experience.institution}",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )

    def test_duration(self) -> None:
        if (experience_end_date := self.experience.end_date) is None:
            self.fail("This test should be run with an experience that has no end date")

        self._assert_actual_end_date_value(self.experience, experience_end_date)
        self._assert_duration_value(self.experience, "2 years, 10 months")


class TestNoEndDateExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=None)

    @patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY_DATE))
    def test_duration(self) -> None:
        self._assert_actual_end_date_value(self.experience, MOCKED_TODAY_DATE)
        self._assert_duration_value(self.experience, "4 years, 11 months")


class TestNoCompanyExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(company="")

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.experience),
            expected_str := self.experience.title,
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )


class TestOnlyMonthsDurationExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2012, 12, 25))

    def test_duration(self) -> None:
        self._assert_duration_value(self.experience, "2 months")


class TestOnlyYearsDurationExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2014, 10, 25))

    def test_duration(self) -> None:
        self._assert_duration_value(self.experience, "2 years")


class TestSingularDurationWordingExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2013, 11, 25))

    def test_duration(self) -> None:
        self._assert_duration_value(self.experience, "1 year, 1 month")


class TestLessThanAMonthExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(start_date=date(2017, 10, 15), end_date=date(2017, 10, 25))

    def test_duration(self) -> None:
        self._assert_duration_value(self.experience, "Less than a month")


class TestNotStartedExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(start_date=date(2017, 10, 25))

    @patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY_DATE))
    def test_duration(self) -> None:
        self._assert_duration_value(self.experience, "Not yet started")


class TestInvalidDatesExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(start_date=date(2017, 10, 25), end_date=date(2017, 10, 24))

    def test_validation_error(self) -> None:
        with self.assertRaises(ValidationError) as cm:
            self.experience.full_clean()

        error = cm.exception.error_dict[NON_FIELD_ERRORS][0]
        self.assertEqual(
            code := error.code, "invalid_dates", f"Expected validation error code 'invalid_dates', got '{code}'"
        )
        self.assertEqual(
            message := error.message,
            "End date must be after start date",
            f"Expected validation error message 'End date must be after start date', got '{message}'",
        )


class TestExperienceTechnologiesRelation(BaseTestExperienceModel):
    tech1: ClassVar[Technology]
    tech2: ClassVar[Technology]
    tech3: ClassVar[Technology]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2015, 8, 29))
        cls.tech1 = Technology.objects.create(name="Tech 1", priority=3)
        cls.tech2 = Technology.objects.create(name="Tech 2", priority=1)
        cls.tech3 = Technology.objects.create(name="Tech 3", priority=2)

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.tech1),
            self.tech1.name,
            f"The __str__ method is returning '{returned_str}' instead the expected value '{self.tech1.name}'",
        )
        self.assertEqual(
            returned_str := str(self.tech2),
            self.tech2.name,
            f"The __str__ method is returning '{returned_str}' instead the expected value '{self.tech2.name}'",
        )
        self.assertEqual(
            returned_str := str(self.tech3),
            self.tech3.name,
            f"The __str__ method is returning '{returned_str}' instead the expected value '{self.tech3.name}'",
        )

    def test_add_technologies_to_experience(self) -> None:
        self.experience.technologies.add(self.tech1, self.tech2)

        self.assertEqual(
            self.experience.technologies.count(),
            2,
            "Experience should have 2 technologies",
        )
        self.assertIn(
            self.tech1,
            self.experience.technologies.all(),
            f"Technology '{self.tech1.name}' should be in experience technologies",
        )
        self.assertIn(
            self.tech2,
            self.experience.technologies.all(),
            f"Technology '{self.tech2.name}' should be in experience technologies",
        )

    def test_remove_technology_from_experience(self) -> None:
        self.experience.technologies.add(self.tech1, self.tech2, self.tech3)
        self.experience.technologies.remove(self.tech2)

        self.assertEqual(
            self.experience.technologies.count(),
            2,
            "Experience should have 2 technologies after removal",
        )
        self.assertNotIn(
            self.tech2,
            self.experience.technologies.all(),
            f"Technology '{self.tech2.name}' should not be in experience technologies after removal",
        )

    def test_technology_reverse_relation(self) -> None:
        self.experience.technologies.add(self.tech1)

        self.assertIn(
            self.experience,
            self.tech1.experiences.all(),
            f"Experience '{self.experience.title}' should be accessible via technology's reverse relation",
        )

    def test_technologies_ordered_by_priority(self) -> None:
        # Add technologies in reverse order to verify they're ordered by priority
        self.experience.technologies.add(self.tech1, self.tech3, self.tech2)

        technologies = list(self.experience.technologies.all())

        self.assertEqual(
            len(technologies),
            3,
            "Experience should have 3 technologies",
        )
        self.assertEqual(
            technologies[0],
            self.tech2,
            f"First technology should be '{self.tech2.name}' (priority {self.tech2.priority}),"
            f" but got '{technologies[0].name}' (priority {technologies[0].priority})",
        )
        self.assertEqual(
            technologies[1],
            self.tech3,
            f"Second technology should be '{self.tech3.name}' (priority {self.tech3.priority}),"
            f" but got '{technologies[1].name}' (priority {technologies[1].priority})",
        )
        self.assertEqual(
            technologies[2],
            self.tech1,
            f"Third technology should be '{self.tech1.name}' (priority {self.tech1.priority}),"
            f" but got '{technologies[2].name}' (priority {technologies[2].priority})",
        )
