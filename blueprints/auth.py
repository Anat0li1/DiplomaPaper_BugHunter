from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User
from utils import hash_password, verify_password
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# Token blocklist. Use Redis or another shared store in production.
blacklisted_tokens = set()

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Зареєструвати нового користувача
    ---
    tags:
      - Автентифікація
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: Користувача успішно зареєстровано
      400:
        description: Бракує полів або email вже зареєстровано
    """
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'error': "Заповніть обов'язкові поля"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Цей email вже зареєстровано'}), 400
    
    password_hash = hash_password(data['password'])
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Користувача успішно зареєстровано'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Вхід користувача
    ---
    tags:
      - Автентифікація
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Вхід виконано успішно
        schema:
          type: object
          properties:
            access_token:
              type: string
            user:
              type: object
      401:
        description: Некоректні облікові дані
    """
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email і пароль обовʼязкові'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not verify_password(data['password'], user.password_hash):
        return jsonify({'error': 'Некоректний email або пароль'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'active_role': user.active_role
        }
    }), 200

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """
    Отримати інформацію про поточного користувача
    ---
    tags:
      - Автентифікація
    security:
      - Bearer: []
    responses:
      200:
        description: Інформація про користувача
        schema:
          type: object
          properties:
            id:
              type: string
            username:
              type: string
            email:
              type: string
            active_role:
              type: string
      404:
        description: Користувача не знайдено
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Користувача не знайдено'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'active_role': user.active_role
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklisted_tokens.add(jti)
    return jsonify({'message': 'Вихід виконано успішно'}), 200

@auth_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_user():
    """
    Оновити профіль користувача
    ---
    tags:
      - Автентифікація
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
            old_password:
              type: string
    responses:
      200:
        description: Користувача успішно оновлено
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Користувача не знайдено'}), 404
    
    data = request.get_json()
    
    if 'username' in data:
        user.username = data['username']
    
    if 'password' in data:
        if 'old_password' not in data:
            return jsonify({'error': 'Поточний пароль обовʼязковий'}), 400
        
        if not verify_password(data['old_password'], user.password_hash):
            return jsonify({'error': 'Поточний пароль некоректний'}), 401
        
        user.password_hash = hash_password(data['password'])
    
    db.session.commit()
    
    return jsonify({'message': 'Користувача успішно оновлено'}), 200

@auth_bp.route('/change_role', methods=['POST'])
@jwt_required()
def change_role():
    """
    Перемкнути роль користувача між user та admin
    ---
    tags:
      - Автентифікація
    security:
      - Bearer: []
    responses:
      200:
        description: Роль успішно змінено
        schema:
          type: object
          properties:
            active_role:
              type: string
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Користувача не знайдено'}), 404
    
    # Toggle between user and admin.
    user.active_role = 'admin' if user.active_role == 'user' else 'user'
    db.session.commit()
    
    return jsonify({
        'message': 'Роль успішно змінено',
        'active_role': user.active_role
    }), 200
