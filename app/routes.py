from flask import Blueprint, request, jsonify
from .models import db, User, Wallet, Transaction  # noqa: F401
from flask_cors import CORS

main = Blueprint('main', __name__)

CORS(main, resources={r"*": {"origins": "*"}})


@main.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@main.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or not data.get('phone'):
        return jsonify({'message': 'No phone number provided'}), 400

    if User.query.filter_by(phone=data['phone']).first():
        return jsonify({'message': 'User already exists'}), 409

    # Create new user
    new_user = User(phone=data['phone'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully',
                    'user': {'id': new_user.id, 'phone': new_user.phone}}), 201
