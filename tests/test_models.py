from app.models import User, Wallet, Transaction


def test_new_user(test_db):
    user = User(phone='1234567890')
    test_db.session.add(user)
    test_db.session.commit()
    assert user.id is not None
    assert user.phone == '1234567890'


def test_new_wallet(test_db):
    user = User(phone='0987654321')
    test_db.session.add(user)
    test_db.session.commit()

    wallet = Wallet(user_id=user.id, wallet_type='savings', balance=100.0,
                    minimum_balance=50.0)
    test_db.session.add(wallet)
    test_db.session.commit()

    assert wallet.id is not None
    assert wallet.user_id == user.id
    assert wallet.wallet_type == 'savings'
    assert wallet.balance == 100.0
    assert wallet.minimum_balance == 50.0


def test_new_transaction(test_db):
    user = User(phone='1122334455')
    test_db.session.add(user)
    test_db.session.commit()

    wallet = Wallet(user_id=user.id, wallet_type='checking', balance=200.0, minimum_balance=20.0)
    test_db.session.add(wallet)
    test_db.session.commit()

    transaction = Transaction(wallet_id=wallet.id, amount=150.0, transaction_type='credit')
    test_db.session.add(transaction)
    test_db.session.commit()

    assert transaction.id is not None
    assert transaction.wallet_id == wallet.id
    assert transaction.amount == 150.0
    assert transaction.transaction_type == 'credit'
    assert transaction.timestamp is not None
