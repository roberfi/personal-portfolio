import os

import dj_database_url

from cv_personal_page.settings.base import *

DEBUG = False

if RENDER_EXTERNAL_HOSTNAME := os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
    )
}

# Add "whitenoise.middleware.WhiteNoiseMiddleware" to the MIDDLEWARE list, immediately after SecurityMiddleware
MIDDLEWARE.insert(
    MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,
    "whitenoise.middleware.WhiteNoiseMiddleware",
)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.dropbox.DropboxStorage",
    },
    "staticfiles": {
        # TODO: use when https://github.com/evansd/whitenoise/issues/561 is fixed
        # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DROPBOX_OAUTH2_REFRESH_TOKEN = os.getenv("DROPBOX_OAUTH2_REFRESH_TOKEN")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
