from app.models import User, Wallet
from app.extensions import db
from services.wallet_service import WalletService
import json


def test_create_user(test_client):
    """Test creating a new user via POST request."""
    response = test_client.post('/user', json={'phone': '12345672290'})
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'


def test_create_wallet(test_client):
    """Testing creating a new wallet via POST request."""
    user = User(phone='1234567890')
    db.session.add(user)
    db.session.commit()
    response = test_client.post('/wallet', json={'user_id': user.id, 'wallet_type': 'standard'})

    # Check if the request was successful (status code 201) and if the wallet was created
    assert response.status_code == 201
    assert Wallet.query.filter_by(user_id=user.id, wallet_type='standard').first() is not None


def test_wallet_balance(test_client):
    # Create a wallet
    response = test_client.post('/user', json={'phone': '1234567890'})
    assert response.status_code == 201
    data = json.loads(response.data)
    user_id = data['user']['id']
    response = test_client.post('/wallet', json={'user_id': user_id, 'wallet_type': 'standard'})
    assert response.status_code == 201
    data = json.loads(response.data)
    wallet_id = data['wallet_id']

    print(wallet_id, Wallet.query.all())

    # Test getting balance for existing wallet
    response = test_client.get(f'/wallet/{wallet_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'balance' in data


def test_credit_wallet(test_client):
    # Create a wallet
    response = test_client.post('/user', json={'phone': '1234567890'})
    assert response.status_code == 201
    data = json.loads(response.data)
    user_id = data['user']['id']
    response = test_client.post('/wallet', json={'user_id': user_id, 'wallet_type': 'standard'})
    assert response.status_code == 201
    data = json.loads(response.data)
    wallet_id = data['wallet_id']

    # Test crediting wallet with valid amount
    response = test_client.post(f'/wallet/{wallet_id}/credit', json={'amount': 100})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data

    # TODO Test crediting wallet with invalid amount, Need to handle this case
    response = test_client.post(f'/wallet/{wallet_id}/credit', json={'amount': -100})
    assert response.status_code == 200
    data = json.loads(response.data)


def test_debit_wallet(test_client):
    # Create a wallet
    response = test_client.post('/user', json={'phone': '1234567890'})
    assert response.status_code == 201
    data = json.loads(response.data)
    user_id = data['user']['id']
    response = test_client.post('/wallet', json={'user_id': user_id, 'wallet_type': 'standard'})
    assert response.status_code == 201
    data = json.loads(response.data)
    wallet_id = data['wallet_id']
    WalletService.credit_wallet(1, 3000)

    # Test debiting wallet with valid amount
    response = test_client.post(f'/wallet/{wallet_id}/debit', json={'amount': 5})
    print(response.data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data

    # # TODO Test debiting wallet with invalid amount, Need to handle this case
    response = test_client.post(f'/wallet/{wallet_id}/debit', json={'amount': 200})
    assert response.status_code == 200
