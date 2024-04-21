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
