"""This is the project's configuration file."""

from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project's root folder path (../).
ROOT_PATH = Path(__file__).resolve().parent.parent

# Project's module folder path (this folder).
PROJECT_PATH = Path(__file__).resolve().parent

# If debug mode is disabled, the app will run in production mode.
DEBUG = True

# Production database URI.
DATABASE_URI = getenv("DATABASE_URI", "sqlite:///./database.db")

# Production database URI.
TESTS_DATABASE_URI = getenv("DATABASE_URI", "sqlite:///./tests.db")

# Add your applications here.
APPS = [
    "tasks",
]
