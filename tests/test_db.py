from sqlalchemy import select

from biblioteca_fastapi.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(username='test', email='test@test', password='secret')

        session.add(user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))

    assert user.id == 1
    assert user.username == 'test'
    assert user.email == 'test@test'
    assert user.password == 'secret'
    assert user.created_at == time
    assert user.updated_at == time
