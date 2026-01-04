from __future__ import annotations

from datetime import date
from typing import ClassVar
from unittest.mock import patch

from django.forms import ValidationError
from django.test import TestCase

from home.models import DatedModel, Experience, SubProject, Technology
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
            self.assertEqual(cm.exception.code, "invalid_dates")
            self.assertEqual(cm.exception.message, "End date must be after start date")


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
            expected_str := f"{self.tech1.name} (Priority: {self.tech1.priority})",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )
        self.assertEqual(
            returned_str := str(self.tech2),
            expected_str := f"{self.tech2.name} (Priority: {self.tech2.priority})",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )
        self.assertEqual(
            returned_str := str(self.tech3),
            expected_str := f"{self.tech3.name} (Priority: {self.tech3.priority})",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
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


class TestExperienceSubProjectsRelation(BaseTestExperienceModel):
    subproject1: ClassVar[SubProject]
    subproject2: ClassVar[SubProject]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2015, 8, 29))
        cls.subproject1 = SubProject.objects.create(
            experience=cls.experience,
            title="SubProject 1",
            client="Client A",
            description="Description 1",
            start_date=date(2013, 1, 1),
            end_date=date(2013, 6, 30),
        )
        cls.subproject2 = SubProject.objects.create(
            experience=cls.experience,
            title="SubProject 2",
            description="Description 2",
            start_date=date(2014, 1, 1),
            end_date=date(2014, 12, 31),
        )

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.subproject1),
            expected_str := f"{self.subproject1.title} at {self.subproject1.client}",
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )
        self.assertEqual(
            returned_str := str(self.subproject2),
            expected_str := self.subproject2.title,
            f"The __str__ method is returning '{returned_str}' instead the expected value '{expected_str}'",
        )

    def test_experience_has_sub_projects(self) -> None:
        self.assertEqual(
            self.experience.sub_projects.count(),
            2,
            "Experience should have 2 sub-projects",
        )
        self.assertIn(
            self.subproject1,
            self.experience.sub_projects.all(),
            f"SubProject '{self.subproject1.title}' should be in experience sub-projects",
        )
        self.assertIn(
            self.subproject2,
            self.experience.sub_projects.all(),
            f"SubProject '{self.subproject2.title}' should be in experience sub-projects",
        )

    def test_sub_project_deletion_does_not_delete_experience(self) -> None:
        subproject_count_before = self.experience.sub_projects.count()
        self.subproject1.delete()

        self.assertTrue(
            Experience.objects.filter(pk=self.experience.pk).exists(),
            f"Experience '{self.experience.title}' should still"
            f" exist after deleting sub-project '{self.subproject1.title}'",
        )
        self.assertEqual(
            self.experience.sub_projects.count(),
            subproject_count_before - 1,
            f"Sub-project count should be {subproject_count_before - 1} but got {self.experience.sub_projects.count()}",
        )

    def test_experience_deletion_cascades_to_sub_projects(self) -> None:
        subproject1_id = self.subproject1.pk
        subproject2_id = self.subproject2.pk
        subproject1_title = self.subproject1.title
        subproject2_title = self.subproject2.title

        self.experience.delete()

        self.assertFalse(
            SubProject.objects.filter(pk=subproject1_id).exists(),
            f"SubProject '{subproject1_title}' (id={subproject1_id})"
            " should be deleted when experience is deleted (CASCADE)",
        )
        self.assertFalse(
            SubProject.objects.filter(pk=subproject2_id).exists(),
            f"SubProject '{subproject2_title}' (id={subproject2_id})"
            " should be deleted when experience is deleted (CASCADE)",
        )


class TestSubProjectDuration(BaseTestExperienceModel):
    @staticmethod
    def _get_new_sub_project_instance(*, start_date: date, end_date: date | None = None) -> SubProject:
        return SubProject.objects.create(
            title=TEST_TITLE,
            client="Test Client",
            description=TEST_DESCRIPTION,
            start_date=start_date,
            end_date=end_date,
        )

    @classmethod
    def setUpTestData(cls) -> None:
        cls.experience = cls._get_new_experience_instance(end_date=date(2015, 8, 29))

    def test_subproject_duration_years_and_months(self) -> None:
        subproject = self._get_new_experience_instance(start_date=date(2013, 1, 15), end_date=date(2015, 11, 20))
        self._assert_actual_end_date_value(subproject, date(2015, 11, 20))
        self._assert_duration_value(subproject, "2 years, 10 months")

    def test_subproject_duration_only_months(self) -> None:
        subproject = self._get_new_experience_instance(start_date=date(2013, 3, 1), end_date=date(2013, 8, 15))
        self._assert_actual_end_date_value(subproject, date(2013, 8, 15))
        self._assert_duration_value(subproject, "5 months")

    def test_subproject_duration_only_years(self) -> None:
        subproject = self._get_new_experience_instance(start_date=date(2013, 6, 1), end_date=date(2015, 6, 1))
        self._assert_actual_end_date_value(subproject, date(2015, 6, 1))
        self._assert_duration_value(subproject, "2 years")

    def test_subproject_duration_less_than_month(self) -> None:
        subproject = self._get_new_experience_instance(start_date=date(2013, 5, 10), end_date=date(2013, 5, 25))
        self._assert_duration_value(subproject, "Less than a month")
        self._assert_actual_end_date_value(subproject, date(2013, 5, 25))

    def test_subproject_duration_no_end_date(self) -> None:
        subproject = self._get_new_experience_instance(start_date=date(2015, 1, 1))

        with patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY_DATE)):
            self._assert_actual_end_date_value(subproject, MOCKED_TODAY_DATE)
            self._assert_duration_value(subproject, "2 years, 8 months")

    def test_not_started_subproject_duration(self) -> None:
        subproject = self._get_new_experience_instance(start_date=date(2017, 10, 1))

        with patch("home.models.datetime.date", get_date_with_mocked_today(MOCKED_TODAY_DATE)):
            self._assert_actual_end_date_value(subproject, MOCKED_TODAY_DATE)
            self._assert_duration_value(subproject, "Not yet started")

    def test_validation_error(self) -> None:
        subproject = self._get_new_experience_instance(start_date=date(2017, 10, 25), end_date=date(2017, 10, 24))
        with self.assertRaises(ValidationError) as cm:
            subproject.full_clean()
            self.assertEqual(cm.exception.code, "invalid_dates")
            self.assertEqual(cm.exception.message, "End date must be after start date")
