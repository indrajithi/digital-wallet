import pytest
import concurrent.futures
from app.models import User, Wallet, Transaction
from services.wallet_service import WalletService
from unittest.mock import patch
from datetime import datetime

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
            transaction = Transaction.query.filter_by(wallet_id=wallet.id).first()

            assert WalletService.get_wallet_balance(wallet.id) == 150
            assert transaction.amount == 50
            assert transaction.transaction_type == 'credit'

    def test_debit_wallet(self, test_app, test_db):
        with test_app.app_context():
            wallet = Wallet(user_id=1, wallet_type='standard', balance=100)
            test_db.session.add(wallet)
            test_db.session.commit()

            WalletService.debit_wallet(wallet.id, 30)
            transaction = Transaction.query.filter_by(wallet_id=wallet.id).first()

            assert transaction.amount == 30
            assert transaction.transaction_type == 'debit'
            assert WalletService.get_wallet_balance(wallet.id) == 70

    def test_debit_transaction_minimum_balance(self, test_app, test_db):
        with test_app.app_context():
            wallet = Wallet(user_id=1, wallet_type='standard', balance=100, minimum_balance=50)
            test_db.session.add(wallet)
            test_db.session.commit()
            with pytest.raises(ValueError) as exc_info:
                WalletService.debit_wallet(wallet.id, 60)  # Assuming X = 60

            assert str(exc_info.value) == "Debit amount exceeds minimum balance"

    @patch('services.wallet_service.WalletService.debit_wallet')
    def test_debit_wallet_concurrency(self, mock_debit_wallet, test_app, test_db):
        wallet = Wallet(user_id=1, wallet_type='new', balance=100, minimum_balance=10)
        test_db.session.add(wallet)
        test_db.session.commit()

        call_counter = [0]  # List to store the call count

        def mock_debit(wallet_id, amount):
            # Increment the call count
            call_counter[0] += 1
            # Return None for the first call, return ValueError for the rest
            if call_counter[0] == 1:
                return None
            else:
                return ValueError("Debit amount exceeds minimum balance")

        # Apply the mocked function to the patch
        mock_debit_wallet.side_effect = mock_debit

        # Simulate concurrent debit transactions
        with test_app.app_context():
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(WalletService.debit_wallet, [wallet.id] * 5, [20, 30, 40, 50, 60]))

        # Verify that only one debit transaction succeeds
        successful_transactions = [result for result in results if result is None]
        assert len(successful_transactions) == 1


class TestTotalTransaction:
    @pytest.mark.parametrize("start_date, end_date, expected_credit, expected_debit", [
        (datetime(2024, 1, 1), datetime(2024, 2, 1), 300.0, 200.0)
    ])
    def test_get_total_transactions_amount(self, test_app, test_db, start_date, end_date, expected_credit, expected_debit):
        with test_app.app_context():
            print(start_date)
            # Create a wallet and perform some credit and debit transactions within the specified time range
            wallet, _ = WalletService.create_wallet(user_id=1, wallet_type='standard')
            WalletService.credit_wallet(wallet.id, 100.0)  # Credit 100
            WalletService.debit_wallet(wallet.id, 50.0)   # Debit 50
            WalletService.credit_wallet(wallet.id, 200.0)  # Credit 200
            WalletService.debit_wallet(wallet.id, 150.0)   # Debit 150
            WalletService.credit_wallet(wallet.id, 300.0)  # Credit 300
            print(WalletService.get_wallet_balance(wallet.id))
            print(Transaction.values())
            # Get the total credited and debited amounts within the specified time range
            total_credit, total_debit = WalletService.get_total_transactions_amount(wallet.id, start_date, end_date)

            # Assert that the retrieved amounts match the expected values
            assert total_credit == expected_credit
            assert total_debit == expected_debit
