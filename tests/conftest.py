from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from biblioteca_fastapi.app import app
from biblioteca_fastapi.database import get_session
from biblioteca_fastapi.models import Base, User


# ele transforma essa função pra ser reutilizada para todos
@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    # Cria no banco as tabelas registradas que ainda não existem
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # apaga tudo
    Base.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(model, time=datetime(2026, 4, 3)):

    def fake_time_hook(mapper, connection, target):
        target.created_at = time
        target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    try:
        yield time
    finally:
        event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    user = User(username='Teste', email='test@test.com', password='mysenha')
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
