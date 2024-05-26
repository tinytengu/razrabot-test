"""Module-level router and its view functions."""

from flask import Blueprint

from project.database import Session
from project.utils.routing import api_view

from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskPartialUpdateSerializer,
)
from . import crud

# Router used in the project for dynamic module/app integration.
router = Blueprint("tasks", __name__)


@router.post("/")
@api_view()
def create_task_view(data: dict | None):
    serializer = TaskCreateSerializer.model_validate(data)

    task = crud.create_task(**serializer.model_dump())
    response = TaskSerializer.model_validate(task).model_dump()

    return response, 201


@router.get("/<task_id>/")
@api_view()
def get_task_view(task_id: str):
    if not (task := crud.get_task(task_id)):
        return {"error": "Invalid task_id"}, 400

    response = TaskSerializer.model_validate(task).model_dump()

    return response


@router.put("/<task_id>/")
@api_view()
def update_task_view(task_id: str, data: dict | None):
    serializer = TaskUpdateSerializer.model_validate(data)

    with Session() as session:
        if not (task := crud.get_task(task_id, session=session)):
            return {"error": "Invalid task_id"}, 400

        crud.udpate_task(task_id, **serializer.model_dump(), session=session)

        response = TaskSerializer.model_validate(task).model_dump()

    return response


@router.patch("/<task_id>/")
@api_view()
def partially_update_task_view(task_id: str, data: dict | None):
    serializer = TaskPartialUpdateSerializer.model_validate(data)

    data = serializer.model_dump(exclude_unset=True)
    if not data:
        return {"error": "Nothing to update"}, 400

    with Session() as session:
        if not (task := crud.get_task(task_id, session=session)):
            return {"error": "Invalid task_id"}, 400

        crud.udpate_task(task_id, **data, session=session)

        response = TaskSerializer.model_validate(task).model_dump()

    return response


@router.delete("/<task_id>/")
@api_view()
def delete_task_view(task_id: str, data: dict | None):
    with Session() as session:
        if not (task := crud.get_task(task_id)):
            return {"error": "Invalid task_id"}, 400

        session.delete(task)
        session.commit()

    return {}, 204


@router.get("/")
@api_view()
def get_tasks_view(data: dict | None):
    response: list[dict] = []

    for task in crud.get_tasks():
        serializer = TaskSerializer.model_validate(task)
        response.append(serializer.model_dump())

    return response


@router.delete("/")
@api_view()
def delete_tasks_view(data: dict | None):
    crud.delete_tasks()
    return [], 204
