from __future__ import annotations

import argparse
import logging
import os

from utils.version_manager.version_manager import VersionManager

COMMAND_READ = "read"
COMMAND_BUMP_DEV = "bump-dev"

GITHUB_OUTPUT = "GITHUB_OUTPUT"

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(description="Manage the versions of the project")
    parser.add_argument(
        "command",
        choices=[COMMAND_READ, COMMAND_BUMP_DEV],
        help="The command to execute",
    )

    parser.add_argument("--current-version", type=str, help="The current version of the project", default=None)

    args = parser.parse_args()

    if args.command == COMMAND_READ:
        result_version = VersionManager.read_current_version().version

        logger.info(f"Current version is: '{result_version}'")

    elif args.command == COMMAND_BUMP_DEV:
        if args.current_version is None:
            parser.error(f"The --current_version argument is required for the '{COMMAND_BUMP_DEV}' command")

        result_version = VersionManager(args.current_version).bump_dev_version()

        logger.info(f"Dev version bumped to: '{result_version}'")

    else:
        parser.error("The command is not recognized")

    if GITHUB_OUTPUT in os.environ:
        with open(os.environ[GITHUB_OUTPUT], "a") as output_file:
            print(f"version={result_version}", file=output_file)
    else:
        logger.warning(f"The '{GITHUB_OUTPUT}' environment variable is not set")
