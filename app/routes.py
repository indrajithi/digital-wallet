from flask import Blueprint, request, jsonify
from .models import db, User, Wallet, Transaction  # noqa: F401
from flask_cors import CORS
from services.user_service import UserService
from services.wallet_service import WalletService
from dateutil import parser


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
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    wallet, error = WalletService.create_wallet(user_id, wallet_type)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'wallet_id': wallet.id}), 201


@main.route('/wallet/<int:wallet_id>', methods=['GET'])
def wallet_balance(wallet_id):
    print("here>>>", wallet_id)
    try:
        balance = WalletService.get_wallet_balance(wallet_id)
        return jsonify({'balance': balance}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@main.route('/wallet/<int:wallet_id>/credit', methods=['POST'])
def credit_wallet(wallet_id):
    amount = request.json.get('amount')
    try:
        WalletService.credit_wallet(wallet_id, amount)
        return jsonify({'message': 'Wallet credited successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@main.route('/wallet/<int:wallet_id>/debit', methods=['POST'])
def debit_wallet(wallet_id):
    amount = request.json.get('amount')
    try:
        WalletService.debit_wallet(wallet_id, amount)
        return jsonify({'message': 'Wallet debited successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@main.route('/wallet/<int:wallet_id>/transactions', methods=['GET'])
def get_wallet_transactions(wallet_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        query = Transaction.query.filter_by(wallet_id=wallet_id)

        if start_date:
            start_date = parser.parse(start_date).date()
            query = query.filter(Transaction.timestamp >= start_date)

        if end_date:
            end_date = parser.parse(end_date).date()
            query = query.filter(Transaction.timestamp <= end_date)

            transactions = [{'id': t.id, 'wallet_id': t.wallet_id, 'amount': t.amount,
                             'transaction_type': t.transaction_type, 'timestamp': t.timestamp.isoformat()} for t in query.all()]

            return jsonify({'transactions': transactions}), 200
    except Exception:
        return jsonify({'error': 'Cannot show the transactions for this wallet. It may not have any transactions!'}), 400
