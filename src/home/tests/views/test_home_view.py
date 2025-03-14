from __future__ import annotations

from django.test import Client, TestCase


class HomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()

    def test_home_view_redirects(self) -> None:
        response = self.client.get("/")
        self.assertRedirects(response, "/en/", status_code=302, target_status_code=200)
