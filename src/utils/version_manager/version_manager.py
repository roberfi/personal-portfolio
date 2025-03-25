from __future__ import annotations

import json
import tomllib

from utils.version_manager.project_version import ProjectVersion

PYPROJECT_TOML_PATH = "../pyproject.toml"
PACKAGE_JSON_PATH = "../package.json"


class VersionManager:
    def __init__(self, version: str) -> None:
        self.__version = ProjectVersion.from_string(version)

    @property
    def version(self) -> ProjectVersion:
        return self.__version

    @classmethod
    def read_current_version(cls) -> VersionManager:
        with open(PYPROJECT_TOML_PATH, "rb") as file:
            toml_data = tomllib.load(file)

            if "project" not in toml_data or "version" not in toml_data["project"]:
                msg = "The current version is not found in pyproject.toml"
                raise ValueError(msg)

            return cls(toml_data["project"]["version"])

    def __write_version_to_pyproject_toml(self) -> None:
        with open(PYPROJECT_TOML_PATH, "r") as file:
            read_data = file.readlines()
            for index, line in enumerate(read_data):
                if "version" in line:
                    read_data[index] = f'version = "{self.__version}"\n'
                    break

        with open(PYPROJECT_TOML_PATH, "w") as file:
            file.writelines(read_data)

    def __write_version_to_package_json(self) -> None:
        with open(PACKAGE_JSON_PATH, "r") as file:
            json_data = json.load(file)
            json_data["version"] = str(self.__version)

        with open(PACKAGE_JSON_PATH, "w") as file:
            json.dump(json_data, file, indent=2)

    def bump_dev_version(self) -> ProjectVersion:
        self.__version = self.__version.bump_dev()
        self.__write_version_to_pyproject_toml()
        self.__write_version_to_package_json()

        return self.__version
