from __future__ import annotations

from django.urls import path

from base.views import LegalAndPrivacyDetailView

urlpatterns = (path("<slug:slug>/", LegalAndPrivacyDetailView.as_view(), name="legal-and-privacy-detail"),)
