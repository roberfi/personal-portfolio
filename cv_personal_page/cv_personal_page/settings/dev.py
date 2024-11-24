from dotenv import load_dotenv

from cv_personal_page.settings.base import *

load_dotenv()

DEBUG = True
ALLOWED_HOSTS: list[str] = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
