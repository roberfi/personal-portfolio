# ruff: noqa: F405 # undefined-local-with-import-star-usage
import os

import dj_database_url

from cv_personal_page.settings.base import *  # noqa: F403 # undefined-local-with-import-star

DEBUG = False
ALLOWED_HOSTS = (os.getenv("RENDER_EXTERNAL_HOSTNAME"),)

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

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.dropbox.DropboxStorage",
        "OPTIONS": {
            "oauth2_refresh_token": os.getenv("DROPBOX_OAUTH2_REFRESH_TOKEN"),
            "app_secret": os.getenv("DROPBOX_APP_SECRET"),
            "app_key": os.getenv("DROPBOX_APP_KEY"),
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
