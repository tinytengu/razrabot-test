from functools import wraps

from flask import request
from pydantic import ValidationError


def validation_error(errors_key: str = "errors"):
    """Decorator that catches Pydantic validation errors (`ValidationError`)
    and returns them as an HTTP 400 (Bad Request) response."""

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationError as e:
                return {errors_key: e.errors()}, 400

        return wrapper

    return inner


def api_view(errors_key: str = "errors"):
    """Decorator that catches Pydantic validation errors (See: `@valdiation_error`)
    and provides parsed JSON request data to the decorated function."""

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs["data"] = request.get_json(silent=True) or None
            try:
                return func(*args, **kwargs)
            except ValidationError as e:
                return {errors_key: e.errors()}, 400

        return wrapper

    return inner
