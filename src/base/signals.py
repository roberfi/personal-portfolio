from __future__ import annotations

from pathlib import Path
from typing import Any

from django.conf import settings
from PIL import Image

# Placeholder images for the SiteMedia defaults, generated after migrations so a fresh
# install works without manually providing media files. Replace them via the admin (Site Media).
DEFAULT_SITE_MEDIA_IMAGES: dict[str, tuple[tuple[int, int], str]] = {
    "portrait.png": ((1920, 1080), "PNG"),
    "favicon.ico": ((32, 32), "ICO"),
    "icon.png": ((64, 64), "PNG"),
}


def create_default_site_media(**kwargs: Any) -> None:
    media_root = Path(settings.MEDIA_ROOT)
    site_media_root = media_root / "site"
    site_media_root.mkdir(parents=True, exist_ok=True)

    for filename, (size, image_format) in DEFAULT_SITE_MEDIA_IMAGES.items():
        path = site_media_root / filename
        if path.exists():
            continue

        legacy_path = media_root / filename
        if legacy_path.exists():
            legacy_path.rename(path)
        else:
            Image.new("RGB", size, color="white").save(path, format=image_format)
