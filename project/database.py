from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    DeclarativeBase,
    Session as SessionType,
)

from project.utils.settings import settings


class Base(DeclarativeBase):
    """Declarative base class for all Pydantic models."""

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"


engine = create_engine(settings.DATABASE_URI)
Session: SessionType = scoped_session(sessionmaker(autoflush=False, bind=engine))


def create_db():
    """Create the database schema."""
    Base.metadata.create_all(bind=engine)


def provide_session(func):
    """Provides `session` argument containing a database session instance to the decorated function.

    If the `session` argument is provided to the wrapped function, it will be used instead of creating a new one and must be closed manually."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get("session") is not None and isinstance(
            kwargs["session"], SessionType
        ):
            return func(*args, **kwargs)

        with Session() as session:
            kwargs["session"] = session
            return func(*args, **kwargs)

    return wrapper
