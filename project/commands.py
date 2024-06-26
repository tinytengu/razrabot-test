"""This file contains CLI commands for the application that are used via `manage.py` script."""

import click
from subprocess import Popen

from .utils.system import get_python_executable
from .utils.settings import settings


@click.command()
def runserver():
    """Runs the Flask server."""
    args = [
        get_python_executable(),
        "-m",
        "flask",
        "--app",
        f"{settings.PROJECT_PATH.name}.application:create_app",
        "run",
        "--reload",
    ]

    if settings.DEBUG is True:
        args.append("--debug")

    Popen(args).wait()


@click.command()
def shell():
    """Runs the interactive Python shell within the project environment."""
    Popen([get_python_executable()]).wait()


@click.command()
def initdb():
    """Initializes the database provided in `settings.DATABASE_URI`."""
    from .database import setup_database

    setup_database()
    click.echo(f"Database initialized (URI: {settings.DATABASE_URI})")


@click.command()
def test():
    """Runs unit tests with Flask application context."""
    import unittest
    from flask import current_app

    with current_app.app_context():
        loader = unittest.TestLoader()
        tests = loader.discover("", top_level_dir=settings.ROOT_PATH)
        testRunner = unittest.TextTestRunner(verbosity=2)
        testRunner.run(tests)
