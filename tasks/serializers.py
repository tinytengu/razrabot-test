from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskSerializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    created_at: datetime
    updated_at: datetime


class TaskCreateSerializer(BaseModel):
    title: str
    description: str


class TaskUpdateSerializer(BaseModel):
    title: str
    description: str


class TaskPartialUpdateSerializer(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
