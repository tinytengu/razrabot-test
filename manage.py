"""This file is used to run flask commands from the terminal without a bunch of flags."""

import sys
from os import environ, getenv
from subprocess import Popen

from project.utils.system import get_python_executable


def main(args: list):
    if len(args) == 0:
        print("Usage: manage.py <command>")
        return

    environ["SETTINGS_MODULE"] = getenv("SETTINGS_MODULE", "project.settings")

    # TODO: This is a hacky way of doing this, but it works for now.
    if args[0] == "test":
        environ["TESTING"] = "1"

    p = Popen(
        [
            get_python_executable(),
            "-m",
            "flask",
            "--app",
            "project.application:create_app",
            *args,
        ]
    )

    p.wait()

    # TODO: This is a hacky way of doing this, but it works for now.
    if getenv("TESTING") == "1":
        from project.database import teardown_database

        teardown_database()


if __name__ == "__main__":
    main(sys.argv[1:])
