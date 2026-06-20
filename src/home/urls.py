from __future__ import annotations

from django.urls import path

from home.views import HomeView, MyCareerView, ProjectDetailView, ProjectListView

urlpatterns = (
    path("", HomeView.as_view(), name="home"),
    path("my-career/", MyCareerView.as_view(), name="my-career"),
    path("projects/", ProjectListView.as_view(), name="projects"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project-detail"),
)
