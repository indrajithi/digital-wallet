import pytest
import concurrent.futures
from app.models import User, Wallet
from services.wallet_service import WalletService


@pytest.fixture
def create_test_user(test_db):
    # Create a test user
    user = User(phone='1234567890')
    test_db.session.add(user)
    test_db.session.commit()
    return user


@pytest.fixture
def wallet(test_db):
    wallet = Wallet(user_id=1, wallet_type='standard', balance=100)
    test_db.session.add(wallet)
    test_db.session.commit()
    return wallet


class TestWalletCreation:
    def test_create_wallet_success(self, create_test_user):
        user = create_test_user
        wallet_type = 'standard'
        wallet, error = WalletService.create_wallet(user.id, wallet_type)

        assert wallet is not None
        assert error is None
        assert wallet.user_id == user.id
        assert wallet.wallet_type == wallet_type

    def test_create_wallet_duplicate_type(self, create_test_user):
        user = create_test_user
        wallet_type = 'standard'

        wallet, error = WalletService.create_wallet(user.id, wallet_type)
        assert wallet is not None
        assert error is None

        # Second wallet creation attempt
        wallet, error = WalletService.create_wallet(user.id, wallet_type)

        # Check if wallet creation fails due to user already having a wallet of the same type
        assert wallet is None
        assert error == 'User already has this type of wallet'

    def test_create_multiple_wallet_of_different_type(self, create_test_user):
        user = create_test_user
        first_wallet_type = 'standard'
        second_first_wallet_type = 'premium'

        # First wallet creation
        wallet, error = WalletService.create_wallet(user.id, first_wallet_type)
        assert wallet is not None
        assert error is None

        # Second wallet creation attempt
        wallet, error = WalletService.create_wallet(user.id, second_first_wallet_type)

        # Check if wallet creation fails due to user already having a wallet of the same type
        assert wallet is not None
        assert error is None


class TestWalletTransactions(object):
    def test_credit_wallet(self, test_app, test_db):
        with test_app.app_context():
            wallet = Wallet(user_id=1, wallet_type='standard', balance=100)
            test_db.session.add(wallet)
            test_db.session.commit()
            WalletService.credit_wallet(wallet.id, 50)
            assert WalletService.get_wallet_balance(wallet.id) == 150

    def test_debit_wallet(self, test_app, test_db):
        with test_app.app_context():
            wallet = Wallet(user_id=1, wallet_type='standard', balance=100)
            test_db.session.add(wallet)
            test_db.session.commit()
            WalletService.debit_wallet(wallet.id, 30)
            assert WalletService.get_wallet_balance(wallet.id) == 70

    def test_debit_wallet_concurrency(self, test_app, test_db):
        # Create a wallet with initial balance and minimum balance
        wallet = Wallet(user_id=1, wallet_type='new', balance=100, minimum_balance=10)
        test_db.session.add(wallet)
        test_db.session.commit()

        # Function to perform debit operation
        def debit(wallet_id, amount):
            try:
                with test_app.app_context():
                    WalletService.debit_wallet(wallet_id, amount)
            except Exception as e:
                return str(e)

        # Simulate concurrent debit transactions
        with test_app.app_context():
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(debit, [wallet.id] * 5, [20, 30, 40, 50, 60]))

        # Verify that only one debit transaction succeeds
        successful_transactions = [result for result in results if result is None]
        assert len(successful_transactions) == 1

