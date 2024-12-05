from django.urls import path

from home.views import background_view, home_view

urlpatterns = [
    path("", home_view),
    path("background.jpg", background_view, name="background"),
]
