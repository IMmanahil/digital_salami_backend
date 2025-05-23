from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app import db
import jwt, datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    required_fields = ['email', 'name', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"Missing '{field}' field"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400

    user = User(email=data['email'], name=data['name'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})
from app.utils.jwt_helper import token_required

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected(current_user_id):
    return jsonify({"message": f"Hello, user {current_user_id}! You reached a protected route."})
