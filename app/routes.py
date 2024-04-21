from flask import Blueprint, request, jsonify
from .models import db, User, Wallet, Transaction  # noqa: F401
from flask_cors import CORS
from services.user_service import UserService
from services.wallet_service import WalletService


main = Blueprint('main', __name__)

CORS(main, resources={r"*": {"origins": "*"}})


@main.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@main.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'phone' not in data:
        return jsonify({'message': 'No phone number provided'}), 400

    try:
        user = UserService.create_user(data['phone'])
        return jsonify({'message': 'User created successfully',
                        'user': {'id': user.id, 'phone': user.phone}}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 409


@main.route('/wallet', methods=['POST'])
def create_wallet():
    user_id = request.json.get('user_id')
    wallet_type = request.json.get('wallet_type')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    wallet, error = WalletService.create_wallet(user_id, wallet_type)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'wallet_id': wallet.id}), 201
