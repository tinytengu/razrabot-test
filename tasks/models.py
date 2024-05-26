"""ORM models."""

from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime

from project.database import Base


def get_uuid_str() -> str:
    """Return randomly generated UUID string."""
    return str(uuid4())


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=get_uuid_str)
    title = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(tz=timezone.utc))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc),
    )
