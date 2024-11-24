from dotenv import load_dotenv

load_dotenv()

from cv_personal_page.settings.base import *  # noqa: E402

DEBUG = True
ALLOWED_HOSTS.append("*")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
