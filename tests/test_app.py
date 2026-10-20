from http import HTTPStatus

from fastapi.testclient import TestClient

from biblioteca_fastapi.app import app


def test_read_api():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola mundo'}
