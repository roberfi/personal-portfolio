from __future__ import annotations

from django.urls import path

from home.views import HomeView, MyCareerView

urlpatterns = (
    path("", HomeView.as_view(), name="home"),
    path("my-career/", MyCareerView.as_view(), name="my-career"),
)
