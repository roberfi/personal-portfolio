from __future__ import annotations

import re
from typing import NamedTuple


class ProjectVersion(NamedTuple):
    major: int
    minor: int
    patch: int
    dev: int | None = None

    @classmethod
    def from_string(cls, version: str) -> ProjectVersion:
        if (result := re.match(r"(\d+)\.(\d+).(\d+)(.dev(\d+))?", version)) is None:
            msg = f"Error reading the version string: '{version}'"
            raise ValueError(msg)

        return cls(
            major=int(result.group(1)),
            minor=int(result.group(2)),
            patch=int(result.group(3)),
            dev=int(result.group(5)) if result.group(5) is not None else None,
        )

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}" + (f".dev{self.dev}" if self.dev is not None else "")

    def bump_dev(self) -> ProjectVersion:
        return ProjectVersion(self.major, self.minor, self.patch, self.dev + 1 if self.dev is not None else 0)
