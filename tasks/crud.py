from sqlalchemy import select, update, delete

from project.database import SessionType, provide_session

from .models import Task


@provide_session
def create_task(**kwargs):
    session: SessionType = kwargs.pop("session")

    task = Task(**kwargs)
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@provide_session
def get_task(task_id: str, **kwargs):
    session: SessionType = kwargs.pop("session")

    query = select(Task).where(Task.id == task_id)
    task = session.scalars(query).first()
    return task


@provide_session
def udpate_task(task_id: str, **kwargs):
    session: SessionType = kwargs.pop("session")

    query = update(Task).where(Task.id == task_id).values(**kwargs)
    session.execute(query)
    session.commit()


@provide_session
def delete_task(task_id: str, **kwargs):
    session: SessionType = kwargs.pop("session")

    query = delete(Task).where(Task.id == task_id)
    session.execute(query)
    session.commit()


@provide_session
def get_tasks(**kwargs):
    session: SessionType = kwargs.pop("session")

    query = select(Task)
    tasks = session.scalars(query).all()

    return tasks


@provide_session
def delete_tasks(**kwargs):
    session: SessionType = kwargs.pop("session")

    query = delete(Task)
    session.execute(query)
    session.commit()
