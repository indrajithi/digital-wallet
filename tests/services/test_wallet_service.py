import pytest
from app.models import User
from services.wallet_service import WalletService


@pytest.fixture
def create_test_user(test_db):
    # Create a test user
    user = User(phone='1234567890')
    test_db.session.add(user)
    test_db.session.commit()
    return user


def test_create_wallet_success(create_test_user):
    user = create_test_user
    wallet_type = 'standard'
    wallet, error = WalletService.create_wallet(user.id, wallet_type)

    assert wallet is not None
    assert error is None
    assert wallet.user_id == user.id
    assert wallet.wallet_type == wallet_type


def test_create_wallet_duplicate_type(create_test_user):
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


def test_create_multiple_wallet_of_different_type(create_test_user):
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
