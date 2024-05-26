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


if __name__ == "__main__":
    main(sys.argv[1:])
