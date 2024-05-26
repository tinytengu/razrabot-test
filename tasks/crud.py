"""Database-related CRUD operations."""

from sqlalchemy import select, update, delete

from project.database import SessionType, provide_session

from .models import Task


@provide_session
def create_task(data: dict, **kwargs):
    """Create a new task.

    Args:
    - data (dict): Task fields to initially set.

    Returns:
    - Task: The created task.
    """
    session: SessionType = kwargs.pop("session")

    task = Task(**data)
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@provide_session
def get_task(task_id: str, **kwargs):
    """Get a task by its ID.

    Args:
    - task_id (str): The ID of the task to get.

    Returns:
    - Task: The task with the given ID, or None if no task with the given ID exists.
    """
    session: SessionType = kwargs.pop("session")

    query = select(Task).where(Task.id == task_id)
    task = session.scalars(query).first()
    return task


@provide_session
def udpate_task(task_id: str, data: dict, **kwargs):
    """Update a task by its ID.

    Args:
    - task_id (str): The ID of the task to update.
    - data (dict): Fields to update the task with.
    """
    session: SessionType = kwargs.pop("session")

    query = update(Task).where(Task.id == task_id).values(**data)
    session.execute(query)
    session.commit()


@provide_session
def delete_task(task_id: str, **kwargs):
    """Delete a task by its ID.

    Args:
    - task_id (str): The ID of the task to delete.
    """
    session: SessionType = kwargs.pop("session")

    query = delete(Task).where(Task.id == task_id)
    session.execute(query)
    session.commit()


@provide_session
def get_tasks(**kwargs):
    """Get all tasks.

    Returns:
    - List[Task]: A list of all tasks.
    """
    session: SessionType = kwargs.pop("session")

    query = select(Task)
    tasks = session.scalars(query).all()

    return tasks


@provide_session
def delete_tasks(**kwargs):
    """Delete all tasks."""
    session: SessionType = kwargs.pop("session")

    query = delete(Task)
    session.execute(query)
    session.commit()
