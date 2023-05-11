from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


class FakeModel(Base):
    __tablename__ = "fake_model"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
