from datetime import datetime
from flask import Blueprint, jsonify, request
from ..services.validators import validate_email

bp = Blueprint('registration', __name__)



@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        errors = []

        username = data.get('username', '').strip()
        if len(username) < 2:
            errors.append('username must be at least 2 characters')
        elif len(username) > 20:
            errors.append('username must not exceed 20 characters')

        email = data.get('email', '').strip()
        if not email:
            errors.append('email is required')
        elif not validate_email(email):
            errors.append('invalid email format')

        password = data.get('password', '')
        if len(password) < 8:
            errors.append('password must be at least 8 characters')

        try:
            age = int(data.get('age', 0))
            if age < 18:
                errors.append('age must be at least 18')
            elif age > 100:
                errors.append('age must not exceed 100')
        except (ValueError, TypeError):
            errors.append('age must be a valid number')

        if errors:
            return jsonify({'errors': errors}), 422

        user = {
            'username': username,
            'email': email,
            'age': age,
            'registered_at': datetime.now().isoformat()
        }

        return jsonify({'message': 'Registration successful', 'user': user}), 201
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
