from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0)
    commission_rate = db.Column(db.Float, default=0.02)  # 2% комиссия
    webhook_url = db.Column(db.String(255))
    role = db.Column(db.String(50), default='user')  # admin or user
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.id} {self.balance}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    commission = db.Column(db.Float)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, canceled, expired
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.id} {self.status}>'

    def calculate_commission(self):
        self.commission = self.amount * self.user.commission_rate