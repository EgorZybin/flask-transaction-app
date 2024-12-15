import pytest
from app import create_app, db
from app.models import User, Transaction

@pytest.fixture
def app():
    app = create_app('testing')  # Будет использовать тестовую конфигурацию
    with app.app_context():
        db.create_all()  # Создаем все таблицы
    yield app
    with app.app_context():
        db.drop_all()  # Удаляем таблицы после тестов

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user(client):
    response = client.post('/users', json={"balance": 100.0, "commission_rate": 0.02, "role": "user"})
    data = response.get_json()
    assert response.status_code == 201
    assert data['balance'] == 100.0
    assert data['commission_rate'] == 0.02
    assert data['role'] == 'user'

def test_create_transaction(client):
    user = User(balance=100.0, commission_rate=0.02)
    db.session.add(user)
    db.session.commit()

    response = client.post('/create_transaction', json={"amount": 50.0, "user_id": user.id})
    data = response.get_json()
    assert response.status_code == 201
    assert data['amount'] == 50.0
    assert data['commission'] == 1.0  # 2% от 50.0

def test_cancel_transaction(client):
    user = User(balance=100.0, commission_rate=0.02)
    db.session.add(user)
    db.session.commit()

    transaction = Transaction(amount=50.0, user_id=user.id)
    db.session.add(transaction)
    db.session.commit()

    response = client.post('/cancel_transaction', json={"transaction_id": transaction.id})
    data = response.get_json()
    assert response.status_code == 200
    assert data['status'] == 'Transaction canceled'

def test_check_transaction(client):
    user = User(balance=100.0, commission_rate=0.02)
    db.session.add(user)
    db.session.commit()

    transaction = Transaction(amount=50.0, user_id=user.id)
    db.session.add(transaction)
    db.session.commit()

    response = client.get(f'/check_transaction?transaction_id={transaction.id}')
    data = response.get_json()
    assert response.status_code == 200
    assert data['transaction_id'] == transaction.id
    assert data['status'] == 'pending'