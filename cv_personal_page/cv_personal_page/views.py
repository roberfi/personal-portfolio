from django.core.files.storage import default_storage
from django.http import HttpRequest, HttpResponse


def favicon_view(request: HttpRequest) -> HttpResponse:
    with default_storage.open("favicon.ico", "rb") as favicon:
        return HttpResponse(favicon.read(), content_type="image/x-icon")
