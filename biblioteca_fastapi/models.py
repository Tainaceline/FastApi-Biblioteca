from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        default=func.now(),
    )
    update = Column(
        DateTime,
        default=func.now(),
    )

    def __init__(self, username, email, password, ativo=True):
        self.username = username
        self.email = email
        self.password = password
        self.ativo = ativo
