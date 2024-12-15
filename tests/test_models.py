from app.models import User, Transaction, db
from datetime import datetime, timedelta


def test_user_model():
    user = User(balance=100.0, commission_rate=0.02)
    db.session.add(user)
    db.session.commit()

    assert user.balance == 100.0
    assert user.commission_rate == 0.02


def test_transaction_model():
    user = User(balance=100.0, commission_rate=0.02)
    db.session.add(user)
    db.session.commit()

    transaction = Transaction(amount=50.0, user_id=user.id)
    transaction.calculate_commission()
    db.session.add(transaction)
    db.session.commit()

    assert transaction.amount == 50.0
    assert transaction.commission == 1.0  # 2% от 50.0
    assert transaction.status == 'pending'


def test_transaction_expiration():
    user = User(balance=100.0, commission_rate=0.02)
    db.session.add(user)
    db.session.commit()

    transaction = Transaction(amount=50.0, user_id=user.id, timestamp=datetime.utcnow() - timedelta(minutes=16))
    db.session.add(transaction)
    db.session.commit()

    assert transaction.status == 'expired'
