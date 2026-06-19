from __future__ import annotations

from typing import ClassVar, NamedTuple

from django.db import IntegrityError
from django.test import TestCase

from home.models import DEFAULT_SERVICE_ICON_PATH, SERVICE_ICON_PATHS, Service

TEST_TITLE = "Web Development"
TEST_SLUG = "web-development"
TEST_SHORT_DESCRIPTION = "Custom websites tailored to your business"
TEST_LONG_DESCRIPTION = "Full-stack web development using Django and modern frontend tools."


class ServiceFields(NamedTuple):
    title: str = TEST_TITLE
    slug: str = TEST_SLUG
    short_description: str = TEST_SHORT_DESCRIPTION
    long_description: str = TEST_LONG_DESCRIPTION
    icon_name: str = ""
    order: int = 0
    is_active: bool = True


class BaseTestServiceModel(TestCase):
    service: ClassVar[Service]

    @staticmethod
    def _make(fields: ServiceFields = ServiceFields()) -> Service:
        return Service.objects.create(
            title=fields.title,
            slug=fields.slug,
            short_description=fields.short_description,
            long_description=fields.long_description,
            icon_name=fields.icon_name,
            order=fields.order,
            is_active=fields.is_active,
        )


class TestServiceModel(BaseTestServiceModel):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.service = cls._make()

    def test_str(self) -> None:
        self.assertEqual(
            returned_str := str(self.service),
            TEST_TITLE,
            f"The __str__ method is returning '{returned_str}' instead of the expected '{TEST_TITLE}'",
        )

    def test_default_is_active_is_true(self) -> None:
        self.assertTrue(
            self.service.is_active,
            "Service 'is_active' field should default to True",
        )

    def test_default_order_is_zero(self) -> None:
        self.assertEqual(
            self.service.order,
            0,
            f"Service 'order' field should default to 0, got {self.service.order}",
        )

    def test_default_icon_name_is_empty(self) -> None:
        self.assertEqual(
            self.service.icon_name,
            "",
            f"Service 'icon_name' field should default to empty string, got '{self.service.icon_name}'",
        )

    def test_icon_path_defaults_when_icon_name_is_blank(self) -> None:
        self.assertEqual(
            icon_path := self.service.icon_path,
            DEFAULT_SERVICE_ICON_PATH.path,
            f"A service with a blank icon_name should fall back to the default icon path, got '{icon_path}'",
        )

    def test_icon_path_maps_known_icon_name(self) -> None:
        service = self._make(ServiceFields(slug="with-icon", icon_name="code"))
        self.assertEqual(
            icon_path := service.icon_path,
            SERVICE_ICON_PATHS["code"].path,
            f"A service with icon_name 'code' should map to its SVG path, got '{icon_path}'",
        )

    def test_icon_path_defaults_when_icon_name_is_unknown(self) -> None:
        service = self._make(ServiceFields(slug="unknown-icon", icon_name="not-a-real-icon"))
        self.assertEqual(
            icon_path := service.icon_path,
            DEFAULT_SERVICE_ICON_PATH.path,
            f"A service with an unknown icon_name should fall back to the default icon path, got '{icon_path}'",
        )

    def test_slug_is_unique(self) -> None:
        with self.assertRaises(
            IntegrityError, msg="Creating a service with a duplicate slug should raise IntegrityError"
        ):
            Service.objects.create(
                title="Another Service",
                slug=TEST_SLUG,
                short_description=TEST_SHORT_DESCRIPTION,
                long_description=TEST_LONG_DESCRIPTION,
            )


class TestServiceOrdering(BaseTestServiceModel):
    service_a: ClassVar[Service]
    service_b: ClassVar[Service]
    service_c: ClassVar[Service]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.service_a = cls._make(ServiceFields(title="Alpha", slug="alpha", order=2))
        cls.service_b = cls._make(ServiceFields(title="Beta", slug="beta", order=1))
        cls.service_c = cls._make(ServiceFields(title="Gamma", slug="gamma", order=1))

    def test_ordered_by_order_then_title(self) -> None:
        services = list(Service.objects.filter(slug__in=("alpha", "beta", "gamma")))

        self.assertEqual(
            services[0],
            self.service_b,
            f"First service should be 'Beta' (order=1), got '{services[0].title}'",
        )
        self.assertEqual(
            services[1],
            self.service_c,
            f"Second service should be 'Gamma' (order=1, alphabetically after Beta), got '{services[1].title}'",
        )
        self.assertEqual(
            services[2],
            self.service_a,
            f"Third service should be 'Alpha' (order=2), got '{services[2].title}'",
        )


class TestServiceActiveFilter(BaseTestServiceModel):
    active_service: ClassVar[Service]
    inactive_service: ClassVar[Service]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.active_service = cls._make(ServiceFields(title="Active", slug="active", is_active=True))
        cls.inactive_service = cls._make(ServiceFields(title="Inactive", slug="inactive", is_active=False))

    def test_active_service(self) -> None:
        self.assertTrue(
            self.active_service.is_active,
            "Service created with is_active=True should have is_active=True",
        )

    def test_inactive_service(self) -> None:
        self.assertFalse(
            self.inactive_service.is_active,
            "Service created with is_active=False should have is_active=False",
        )

    def test_filter_active(self) -> None:
        active = list(Service.objects.filter(is_active=True))
        self.assertIn(
            self.active_service,
            active,
            f"Active service '{self.active_service.title}' should appear in is_active=True queryset",
        )
        self.assertNotIn(
            self.inactive_service,
            active,
            f"Inactive service '{self.inactive_service.title}' should not appear in is_active=True queryset",
        )
