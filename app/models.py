from .extensions import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wallet_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    minimum_balance = db.Column(db.Float, default=50.0)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'),
                          nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
