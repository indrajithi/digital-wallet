from flask import Blueprint, request, jsonify
from .models import db, User, Wallet, Transaction  # noqa: F401
from flask_cors import CORS
from services.user_service import UserService


main = Blueprint('main', __name__)

CORS(main, resources={r"*": {"origins": "*"}})


@main.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@main.route('/create_user', methods=['POST'])
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
