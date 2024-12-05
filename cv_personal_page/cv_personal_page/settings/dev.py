# ruff: noqa: F405 # undefined-local-with-import-star-usage
from cv_personal_page.settings.base import *  # noqa: F403 # undefined-local-with-import-star

DEBUG = True
SECRET_KEY = "django-insecure-hzy@^bafqj6aysq$i+e5udxvc+v!w-%lx^ug&ko9j4=2ndiga_"
ALLOWED_HOSTS = ("*",)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
