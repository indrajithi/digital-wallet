from app.models import Wallet
from app.extensions import db


class WalletService:
    @staticmethod
    def create_wallet(user_id, wallet_type):
        existing_wallet = Wallet.query.filter_by(user_id=user_id, wallet_type=wallet_type).first()
        if existing_wallet:
            return None, 'User already has this type of wallet'

        new_wallet = Wallet(user_id=user_id, wallet_type=wallet_type, balance=0.0, minimum_balance=50.0)
        db.session.add(new_wallet)
        db.session.commit()
        return new_wallet, None

    @staticmethod
    def credit_wallet(wallet_id, amount):
        with db.session.begin_nested():
            wallet = Wallet.query.filter_by(id=wallet_id).with_for_update().one()
            wallet.balance += amount
            db.session.commit()

    @staticmethod
    def debit_wallet(wallet_id, amount):
        with db.session.begin_nested():
            wallet = Wallet.query.filter_by(id=wallet_id).with_for_update().one()
            if wallet.balance - amount < wallet.minimum_balance:
                raise ValueError("Debit amount exceeds minimum balance")
            wallet.balance -= amount
            db.session.commit()

    @staticmethod
    def get_wallet_balance(wallet_id):
        wallet = Wallet.query.filter_by(id=wallet_id).one()
        return wallet.balance
