from app.models import User, Wallet
from app.extensions import db


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
