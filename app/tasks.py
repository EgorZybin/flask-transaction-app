from .extensions import celery
from datetime import datetime, timedelta
from .models import Transaction, db
import requests


@celery.task
def check_expired_transactions():
    now = datetime.utcnow()
    transactions = Transaction.query.filter_by(status='pending').all()

    for transaction in transactions:
        if now - transaction.timestamp > timedelta(minutes=15):
            transaction.status = 'expired'
            db.session.commit()
            # отправка вебхука
            if transaction.user.webhook_url:
                payload = {'transaction_id': transaction.id, 'status': 'expired'}
                requests.post(transaction.user.webhook_url, json=payload)