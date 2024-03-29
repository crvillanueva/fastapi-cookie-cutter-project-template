from typing import List, Type, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import asc, delete, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

T = TypeVar("T")


def create_model_instance(session: Session, SqlModel: Type[T], **kwargs) -> T:
    new_instance = SqlModel(**kwargs)
    session.add(new_instance)
    session.commit()
    session.refresh(new_instance)
    return new_instance


def create_model_instances(
    session: Session, SqlModel: Type[T], new_instances: List[BaseModel]
) -> list[T]:
    new_model_instances = []
    for instance in new_instances:
        new_instance = SqlModel(**instance.dict(exclude_unset=True))
        new_model_instances.append(new_instance)
    session.add_all(new_model_instances)
    session.commit()
    return new_model_instances


def select_unique_from_model(
    session: Session, SqlModel: Type[T], pk: int | str | None = None
) -> T:
    instance = session.get(SqlModel, pk)
    if not instance:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return instance


def select_all_from_model(session: Session, SqlModel: Type[T]) -> list[T]:
    objects = session.execute(select(SqlModel)).scalars().all()
    if not objects:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return objects


def update_model_by_pk(
    session: Session, SqlModel: Type[T], pk: int | str | None, **kwargs
) -> T:
    instance = session.get(SqlModel, pk)
    if not instance:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    for key, value in kwargs.items():
        setattr(instance, key, value)
    session.commit()
    session.refresh(instance)
    return instance


def delete_all(session: Session, SqlModel) -> bool:
    session.execute(delete(SqlModel))
    session.commit()
    return True


def delete_model_by_pk(session: Session, SqlModel: Type[T], pk: int | str) -> bool:
    instance = session.get(SqlModel, pk)
    session.delete(instance)
    session.commit()
    return True


def select_multiple_by_attributes(
    session: Session, SqlModel: Type[T], **kwargs
) -> List[T]:
    instances = session.query(SqlModel).filter_by(**kwargs).all()
    if not instances:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return instances


def delete_by_attributes(session: Session, SqlModel: Type[T], **kwargs) -> bool:
    session.execute(delete(SqlModel).filter_by(**kwargs))
    session.commit()
    return True


def select_unique_by_attribute(session: Session, SqlModel: Type[T], **kwargs) -> T:
    instance = session.query(SqlModel).filter_by(**kwargs).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return instance


def select_by_model_and_order_by(
    session: Session, SqlModel: Type[T], column: str, order: str = "asc"
) -> List[T]:
    if order == "desc":
        objects = (
            session.query(SqlModel).order_by(desc(getattr(SqlModel, column))).all()
        )
    elif order == "asc":
        objects = session.query(SqlModel).order_by(asc(getattr(SqlModel, column))).all()
    return objects
