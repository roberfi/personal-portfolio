from __future__ import annotations

from datetime import date
from typing import ClassVar
from unittest.mock import MagicMock, patch

from django.forms import ValidationError
from django.test import TestCase

from home.models import Experience


class BaseTestExperienceModel(TestCase):
    experience: ClassVar[Experience]

    @staticmethod
    def _get_new_experience_instance(
        *, start_date: date = date(2012, 10, 25), end_date: date | None = None
    ) -> Experience:
        return Experience(
            title="Test Title",
            location="Any Location",
            company="Any Company",
            description="Description of the experience",
            start_date=start_date,
            end_date=end_date,
        )

    def _assert_actual_end_date_value(self, expected_date: date) -> None:
        self.assertEqual(
            actual_end_date := self.experience.actual_end_date,
            expected_date,
            f"The returned actual end date is '{actual_end_date}' instead of the expected '{expected_date}'",
        )

    def _assert_duration_value(self, expected_duration: str) -> None:
        self.assertEqual(
            returned_duration := self.experience.duration,
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
            expected_str := f"{self.experience.title} at {self.experience.company}",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )

    def test_actual_end_date(self) -> None:
        if (experience_end_date := self.experience.end_date) is None:
            self.fail("This test should be run with an experience that has no end date")

        self._assert_actual_end_date_value(experience_end_date)

    def test_duration(self) -> None:
        self._assert_duration_value("2 years, 10 months")


class TestNoEndDateExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=None)

    @patch("home.models.datetime.date")
    def test_actual_end_date(self, mock_date: MagicMock) -> None:
        mock_date.today.return_value = date(2017, 9, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        self._assert_actual_end_date_value(date(2017, 9, 15))

    @patch("home.models.datetime.date")
    def test_duration(self, mock_date: MagicMock) -> None:
        mock_date.today.return_value = date(2017, 9, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        self._assert_duration_value("4 years, 11 months")


class TestOnlyMonthsDurationExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2012, 12, 25))

    def test_duration(self) -> None:
        self._assert_duration_value("2 months")


class TestOnlyYearsDurationExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2014, 10, 25))

    def test_duration(self) -> None:
        self._assert_duration_value("2 years")


class TestSingularDurationWordingExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2013, 11, 25))

    def test_duration(self) -> None:
        self._assert_duration_value("1 year, 1 month")


class TestLessThanAMonthExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(start_date=date(2017, 10, 15), end_date=date(2017, 10, 25))

    def test_duration(self) -> None:
        self._assert_duration_value("Less than a month")


class TestNotStartedExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(start_date=date(2017, 10, 25))

    @patch("home.models.datetime.date")
    def test_duration(self, mock_date: MagicMock) -> None:
        mock_date.today.return_value = date(2017, 9, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        self._assert_duration_value("Not yet started")


class TesInvalidDatesExperienceModel(BaseTestExperienceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(start_date=date(2017, 10, 25), end_date=date(2017, 10, 24))

    def test_validation_error(self) -> None:
        with self.assertRaises(ValidationError) as cm:
            self.experience.full_clean()
            self.assertEqual(cm.exception.code, "invalid_dates")
            self.assertEqual(cm.exception.message, "End date must be after start date")
