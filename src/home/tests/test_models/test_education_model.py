from __future__ import annotations

from datetime import date
from typing import ClassVar
from unittest.mock import patch

from django.forms import ValidationError
from django.test import TestCase

from home.models import Education
from utils.test_utils.mocks import get_date_with_mocked_today

# Constants
TEST_TITLE = "Test Education Title"
TEST_INSTITUTION = "Test Institution"
TEST_LOCATION = "Test Location"
TEST_DESCRIPTION = "Description of the education"
DEFAULT_START_DATE = date(2010, 9, 1)

MOCKED_TODAY_DATE = date(2017, 9, 15)


class BaseTestEducationModel(TestCase):
    education: ClassVar[Education]

    @staticmethod
    def _get_new_education_instance(
        *, start_date: date = DEFAULT_START_DATE, end_date: date | None = None
    ) -> Education:
        return Education(
            title=TEST_TITLE,
            institution=TEST_INSTITUTION,
            location=TEST_LOCATION,
            description=TEST_DESCRIPTION,
            start_date=start_date,
            end_date=end_date,
        )

    def _assert_actual_end_date_value(self, expected_date: date) -> None:
        self.assertEqual(
            actual_end_date := self.education.actual_end_date,
            expected_date,
            f"The returned actual end date is '{actual_end_date}' instead of the expected '{expected_date}'",
        )

    def _assert_duration_value(self, expected_duration: str) -> None:
        self.assertEqual(
            returned_duration := self.education.duration,
            expected_duration,
            f"The returned duration is '{returned_duration}' instead of the expected '{expected_duration}'",
        )


class TestEducationModel(BaseTestEducationModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.education = cls._get_new_education_instance(end_date=date(2014, 6, 30))

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.education),
            expected_str := f"{self.education.title} at {self.education.institution}",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )

    def test_actual_end_date(self) -> None:
        if (education_end_date := self.education.end_date) is None:
            self.fail("This test should be run with an education that has an end date")

        self._assert_actual_end_date_value(education_end_date)

    def test_duration(self) -> None:
        self._assert_duration_value("3 years, 9 months")


class TestNoEndDateEducationModel(BaseTestEducationModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.education = cls._get_new_education_instance(end_date=None)

    @patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY_DATE))
    def test_actual_end_date(self) -> None:
        self._assert_actual_end_date_value(MOCKED_TODAY_DATE)

    @patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY_DATE))
    def test_duration(self) -> None:
        self._assert_duration_value("7 years")


class TestOnlyMonthsDurationEducationModel(BaseTestEducationModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.education = cls._get_new_education_instance(end_date=date(2010, 11, 1))

    def test_duration(self) -> None:
        self._assert_duration_value("2 months")


class TestOnlyYearsDurationEducationModel(BaseTestEducationModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.education = cls._get_new_education_instance(end_date=date(2013, 9, 1))

    def test_duration(self) -> None:
        self._assert_duration_value("3 years")


class TestSingularDurationWordingEducationModel(BaseTestEducationModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.education = cls._get_new_education_instance(end_date=date(2011, 10, 1))

    def test_duration(self) -> None:
        self._assert_duration_value("1 year, 1 month")


class TestLessThanAMonthEducationModel(BaseTestEducationModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.education = cls._get_new_education_instance(start_date=date(2017, 10, 15), end_date=date(2017, 10, 25))

    def test_duration(self) -> None:
        self._assert_duration_value("Less than a month")


class TestNotStartedEducationModel(BaseTestEducationModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.education = cls._get_new_education_instance(start_date=date(2017, 10, 25))

    @patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY_DATE))
    def test_duration(self) -> None:
        self._assert_duration_value("Not yet started")


class TestInvalidDatesEducationModel(BaseTestEducationModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.education = cls._get_new_education_instance(start_date=date(2017, 10, 25), end_date=date(2017, 10, 24))

    def test_validation_error(self) -> None:
        with self.assertRaises(ValidationError) as cm:
            self.education.full_clean()
            self.assertEqual(cm.exception.code, "invalid_dates")
            self.assertEqual(cm.exception.message, "End date must be after start date")
