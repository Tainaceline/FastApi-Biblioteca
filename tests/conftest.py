from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from biblioteca_fastapi.app import app
from biblioteca_fastapi.models import Base


# ele transforma essa função pra ser reutilizada para todos
@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
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

    event.listen(model, 'before_insert', fake_time_hook)

    try:
        yield time
    finally:
        event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
