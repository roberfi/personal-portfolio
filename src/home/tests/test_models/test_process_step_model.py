from __future__ import annotations

from typing import ClassVar, NamedTuple

from django.test import TestCase

from home.models import ProcessStep

TEST_TITLE = "Descubrimiento"
TEST_DESCRIPTION = "Analizamos tus necesidades y definimos el alcance del proyecto."


class ProcessStepFields(NamedTuple):
    title: str = TEST_TITLE
    description: str = TEST_DESCRIPTION
    icon_name: str = ""
    order: int = 0


class BaseTestProcessStepModel(TestCase):
    step: ClassVar[ProcessStep]

    @staticmethod
    def _make(fields: ProcessStepFields = ProcessStepFields()) -> ProcessStep:
        return ProcessStep.objects.create(
            title=fields.title,
            description=fields.description,
            icon_name=fields.icon_name,
            order=fields.order,
        )


class TestProcessStepModel(BaseTestProcessStepModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.step = cls._make()

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.step),
            TEST_TITLE,
            f"The __str__ method is returning '{returned_str}' instead of the expected '{TEST_TITLE}'",
        )

    def test_default_order_is_zero(self) -> None:
        self.assertEqual(
            self.step.order,
            0,
            f"ProcessStep 'order' field should default to 0, got {self.step.order}",
        )

    def test_default_icon_name_is_empty(self) -> None:
        self.assertEqual(
            self.step.icon_name,
            "",
            f"ProcessStep 'icon_name' field should default to empty string, got '{self.step.icon_name}'",
        )


class TestProcessStepOrdering(BaseTestProcessStepModel):
    step_1: ClassVar[ProcessStep]
    step_2: ClassVar[ProcessStep]
    step_3: ClassVar[ProcessStep]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.step_1 = cls._make(ProcessStepFields(title="Paso 1", order=1))
        cls.step_2 = cls._make(ProcessStepFields(title="Paso 2", order=2))
        cls.step_3 = cls._make(ProcessStepFields(title="Paso 3", order=3))

    def test_ordered_by_order(self) -> None:
        steps = list(ProcessStep.objects.filter(title__in=("Paso 1", "Paso 2", "Paso 3")))

        self.assertEqual(
            steps[0],
            self.step_1,
            f"First step should be 'Paso 1' (order=1), got '{steps[0].title}'",
        )
        self.assertEqual(
            steps[1],
            self.step_2,
            f"Second step should be 'Paso 2' (order=2), got '{steps[1].title}'",
        )
        self.assertEqual(
            steps[2],
            self.step_3,
            f"Third step should be 'Paso 3' (order=3), got '{steps[2].title}'",
        )
