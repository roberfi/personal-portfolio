from __future__ import annotations

from typing import ClassVar, NamedTuple

from django.db import IntegrityError
from django.test import TestCase

from home.models import Project, Technology

TEST_TITLE = "Test Project"
TEST_SLUG = "test-project"
TEST_PROBLEM = "The client had no online presence"
TEST_APPROACH = "Built a Django-based website with Tailwind CSS"
TEST_OUTCOME = "Increased leads by 40% in the first quarter"


class ProjectFields(NamedTuple):
    title: str = TEST_TITLE
    slug: str = TEST_SLUG
    problem: str = TEST_PROBLEM
    approach: str = TEST_APPROACH
    outcome: str = TEST_OUTCOME
    featured: bool = False
    order: int = 0


class BaseTestProjectModel(TestCase):
    project: ClassVar[Project]

    @staticmethod
    def _get_new_project_instance(fields: ProjectFields = ProjectFields()) -> Project:
        return Project.objects.create(
            title=fields.title,
            slug=fields.slug,
            problem=fields.problem,
            approach=fields.approach,
            outcome=fields.outcome,
            featured=fields.featured,
            order=fields.order,
        )


class TestProjectModel(BaseTestProjectModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.project = cls._get_new_project_instance()

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.project),
            TEST_TITLE,
            f"The __str__ method is returning '{returned_str}' instead of the expected '{TEST_TITLE}'",
        )

    def test_default_featured_is_false(self) -> None:
        self.assertFalse(
            self.project.featured,
            "Project 'featured' field should default to False",
        )

    def test_default_order_is_zero(self) -> None:
        self.assertEqual(
            self.project.order,
            0,
            f"Project 'order' field should default to 0, got {self.project.order}",
        )

    def test_slug_is_unique(self) -> None:
        with self.assertRaises(
            IntegrityError, msg="Creating a project with a duplicate slug should raise IntegrityError"
        ):
            Project.objects.create(
                title="Another Project",
                slug=TEST_SLUG,
                problem=TEST_PROBLEM,
                approach=TEST_APPROACH,
                outcome=TEST_OUTCOME,
            )


class TestProjectOrdering(BaseTestProjectModel):
    project_a: ClassVar[Project]
    project_b: ClassVar[Project]
    project_c: ClassVar[Project]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.project_a = cls._get_new_project_instance(ProjectFields(title="Alpha", slug="alpha", order=2))
        cls.project_b = cls._get_new_project_instance(ProjectFields(title="Beta", slug="beta", order=1))
        cls.project_c = cls._get_new_project_instance(ProjectFields(title="Gamma", slug="gamma", order=1))

    def test_ordered_by_order_then_title(self) -> None:
        projects = list(Project.objects.filter(slug__in=("alpha", "beta", "gamma")))

        self.assertEqual(
            projects[0],
            self.project_b,
            f"First project should be 'Beta' (order=1), got '{projects[0].title}'",
        )
        self.assertEqual(
            projects[1],
            self.project_c,
            f"Second project should be 'Gamma' (order=1, alphabetically after Beta), got '{projects[1].title}'",
        )
        self.assertEqual(
            projects[2],
            self.project_a,
            f"Third project should be 'Alpha' (order=2), got '{projects[2].title}'",
        )


class TestProjectFeatured(BaseTestProjectModel):
    featured_project: ClassVar[Project]
    unfeatured_project: ClassVar[Project]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.featured_project = cls._get_new_project_instance(
            ProjectFields(title="Featured", slug="featured", featured=True)
        )
        cls.unfeatured_project = cls._get_new_project_instance(ProjectFields(title="Unfeatured", slug="unfeatured"))

    def test_featured_project(self) -> None:
        self.assertTrue(
            self.featured_project.featured,
            "Project created with featured=True should have featured=True",
        )

    def test_unfeatured_project(self) -> None:
        self.assertFalse(
            self.unfeatured_project.featured,
            "Project created with featured=False should have featured=False",
        )

    def test_filter_featured(self) -> None:
        featured = list(Project.objects.filter(featured=True))
        self.assertIn(
            self.featured_project,
            featured,
            f"Featured project '{self.featured_project.title}' should appear in featured queryset",
        )
        self.assertNotIn(
            self.unfeatured_project,
            featured,
            f"Unfeatured project '{self.unfeatured_project.title}' should not appear in featured queryset",
        )


class TestProjectTechnologiesRelation(BaseTestProjectModel):
    tech1: ClassVar[Technology]
    tech2: ClassVar[Technology]
    tech3: ClassVar[Technology]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.project = cls._get_new_project_instance()
        cls.tech1 = Technology.objects.create(name="Django", priority=1)
        cls.tech2 = Technology.objects.create(name="Python", priority=2)
        cls.tech3 = Technology.objects.create(name="Tailwind", priority=3)

    def test_add_technologies(self) -> None:
        self.project.technologies.add(self.tech1, self.tech2)

        self.assertEqual(
            self.project.technologies.count(),
            2,
            "Project should have 2 technologies after adding them",
        )
        self.assertIn(
            self.tech1,
            self.project.technologies.all(),
            f"Technology '{self.tech1.name}' should be in project technologies",
        )
        self.assertIn(
            self.tech2,
            self.project.technologies.all(),
            f"Technology '{self.tech2.name}' should be in project technologies",
        )

    def test_remove_technology(self) -> None:
        self.project.technologies.set((self.tech1, self.tech2, self.tech3))
        self.project.technologies.remove(self.tech2)

        self.assertEqual(
            self.project.technologies.count(),
            2,
            "Project should have 2 technologies after removing one",
        )
        self.assertNotIn(
            self.tech2,
            self.project.technologies.all(),
            f"Technology '{self.tech2.name}' should not be in project technologies after removal",
        )

    def test_technology_reverse_relation(self) -> None:
        self.project.technologies.add(self.tech1)

        self.assertIn(
            self.project,
            self.tech1.projects.all(),
            f"Project '{self.project.title}' should be accessible via technology's reverse relation",
        )
