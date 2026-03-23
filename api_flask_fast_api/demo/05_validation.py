"""
Flask Demo 5: Data Validation
Demonstrates input validation, error handling, and data sanitization

Usage:
    python 05_validation.py

Testing:
    # Valid registration
    curl -X POST http://localhost:5000/api/register \
      -H "Content-Type: application/json" \
      -d '{"username":"alice","email":"alice@example.com","password":"SecurePass123","age":28}'

    # Invalid email
    curl -X POST http://localhost:5000/api/register \
      -H "Content-Type: application/json" \
      -d '{"username":"alice","email":"invalid-email","password":"SecurePass123","age":28}'

    # Weak password
    curl -X POST http://localhost:5000/api/register \
      -H "Content-Type: application/json" \
      -d '{"username":"alice","email":"alice@example.com","password":"123","age":28}'

    # Update profile
    curl -X PUT http://localhost:5000/api/users/1/profile \
      -H "Content-Type: application/json" \
      -d '{"first_name":"Alice","last_name":"Smith","age":30}'
"""

from flask import Flask, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

# In-memory user database
users_db = {
    1: {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
        "password": "hashed_password_123",
        "age": 28,
        "first_name": "Alice",
        "last_name": "Smith",
        "created_at": "2024-01-15"
    }
}

next_user_id = 2

# Validation patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
USERNAME_PATTERN = r'^[a-zA-Z0-9_]{3,20}$'


# ============================================================================
# Validation Functions
# ============================================================================

def validate_email(email):
    """
    Validate email format

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required and must be a string"

    email = email.strip()
    if len(email) > 254:
        return False, "Email is too long (max 254 characters)"

    if not re.match(EMAIL_PATTERN, email):
        return False, "Invalid email format"

    return True, None


def validate_username(username):
    """
    Validate username (alphanumeric + underscore, 3-20 chars)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not username or not isinstance(username, str):
        return False, "Username is required and must be a string"

    username = username.strip()
    if not re.match(USERNAME_PATTERN, username):
        return False, "Username must be 3-20 characters (letters, numbers, underscore)"

    return True, None


def validate_password(password):
    """
    Validate password strength

    Requirements:
        - At least 8 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 digit
        - At least 1 special character

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least 1 uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least 1 lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least 1 digit"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least 1 special character"

    return True, None


def validate_age(age):
    """
    Validate age (must be integer between 13 and 120)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if age is None:
        return False, "Age is required"

    try:
        age_int = int(age)
    except (ValueError, TypeError):
        return False, "Age must be an integer"

    if age_int < 13:
        return False, "Must be at least 13 years old"

    if age_int > 120:
        return False, "Age cannot exceed 120"

    return True, None


def validate_name(name, field_name="Name"):
    """
    Validate name fields (2-50 characters, letters and spaces only)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, f"{field_name} is required and must be a string"

    name = name.strip()
    if len(name) < 2 or len(name) > 50:
        return False, f"{field_name} must be 2-50 characters"

    if not re.match(r'^[a-zA-Z\s\'-]+$', name):
        return False, f"{field_name} can only contain letters, spaces, hyphens, and apostrophes"

    return True, None


def check_username_exists(username, exclude_id=None):
    """Check if username already exists"""
    for user in users_db.values():
        if user['username'].lower() == username.lower() and user['id'] != exclude_id:
            return True
    return False


def check_email_exists(email, exclude_id=None):
    """Check if email already exists"""
    for user in users_db.values():
        if user['email'].lower() == email.lower() and user['id'] != exclude_id:
            return True
    return False


# ============================================================================
# Endpoints
# ============================================================================

@app.route('/api/register', methods=['POST'])
def register():
    """
    POST /api/register
    Register new user with comprehensive validation

    Required fields:
        - username: 3-20 chars, alphanumeric + underscore
        - email: valid email format
        - password: 8+ chars, uppercase, lowercase, digit, special char
        - age: 13-120

    Returns:
        201: User registered successfully
        400: Validation error
        409: Username or email already exists
    """
    global next_user_id

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json"
        }), 400

    data = request.get_json()

    # Validate required fields
    required = ['username', 'email', 'password', 'age']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({
            "success": False,
            "error": "Missing required fields",
            "missing_fields": missing
        }), 400

    # Validate username
    is_valid, error = validate_username(data['username'])
    if not is_valid:
        return jsonify({
            "success": False,
            "field": "username",
            "error": error
        }), 400

    # Check username doesn't exist
    if check_username_exists(data['username']):
        return jsonify({
            "success": False,
            "field": "username",
            "error": "Username already taken"
        }), 409

    # Validate email
    is_valid, error = validate_email(data['email'])
    if not is_valid:
        return jsonify({
            "success": False,
            "field": "email",
            "error": error
        }), 400

    # Check email doesn't exist
    if check_email_exists(data['email']):
        return jsonify({
            "success": False,
            "field": "email",
            "error": "Email already registered"
        }), 409

    # Validate password
    is_valid, error = validate_password(data['password'])
    if not is_valid:
        return jsonify({
            "success": False,
            "field": "password",
            "error": error
        }), 400

    # Validate age
    is_valid, error = validate_age(data['age'])
    if not is_valid:
        return jsonify({
            "success": False,
            "field": "age",
            "error": error
        }), 400

    # All validations passed - create user
    new_user = {
        "id": next_user_id,
        "username": data['username'],
        "email": data['email'],
        "password": f"hashed_{data['password']}",  # In production, hash the password!
        "age": int(data['age']),
        "first_name": data.get('first_name', ''),
        "last_name": data.get('last_name', ''),
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }

    users_db[next_user_id] = new_user
    next_user_id += 1

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "data": {
            "id": new_user['id'],
            "username": new_user['username'],
            "email": new_user['email'],
            "created_at": new_user['created_at']
        }
    }), 201


@app.route('/api/users/<int:user_id>/profile', methods=['PUT'])
def update_profile(user_id):
    """
    PUT /api/users/:id/profile
    Update user profile with validation

    Optional fields:
        - first_name: 2-50 chars
        - last_name: 2-50 chars
        - age: 13-120
        - email: valid format

    Returns:
        200: Profile updated
        404: User not found
        400: Validation error
    """
    if user_id not in users_db:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json"
        }), 400

    data = request.get_json()
    user = users_db[user_id]

    # Validate optional fields
    if 'first_name' in data:
        is_valid, error = validate_name(data['first_name'], "First name")
        if not is_valid:
            return jsonify({
                "success": False,
                "field": "first_name",
                "error": error
            }), 400
        user['first_name'] = data['first_name']

    if 'last_name' in data:
        is_valid, error = validate_name(data['last_name'], "Last name")
        if not is_valid:
            return jsonify({
                "success": False,
                "field": "last_name",
                "error": error
            }), 400
        user['last_name'] = data['last_name']

    if 'age' in data:
        is_valid, error = validate_age(data['age'])
        if not is_valid:
            return jsonify({
                "success": False,
                "field": "age",
                "error": error
            }), 400
        user['age'] = int(data['age'])

    if 'email' in data:
        is_valid, error = validate_email(data['email'])
        if not is_valid:
            return jsonify({
                "success": False,
                "field": "email",
                "error": error
            }), 400
        if check_email_exists(data['email'], exclude_id=user_id):
            return jsonify({
                "success": False,
                "field": "email",
                "error": "Email already in use"
            }), 409
        user['email'] = data['email']

    return jsonify({
        "success": True,
        "message": "Profile updated",
        "data": user
    }), 200


@app.route('/api/validate', methods=['POST'])
def validate_field():
    """
    POST /api/validate
    Validate a specific field

    JSON body:
        {
            "field": "email|username|password|age|name",
            "value": "...",
            "field_name": "..." (optional, for name validation)
        }

    Returns:
        200: Validation result
    """
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json"
        }), 400

    data = request.get_json()
    field = data.get('field')
    value = data.get('value')

    if not field or value is None:
        return jsonify({
            "success": False,
            "error": "field and value are required"
        }), 400

    # Validate based on field type
    if field == 'email':
        is_valid, error = validate_email(value)
    elif field == 'username':
        is_valid, error = validate_username(value)
    elif field == 'password':
        is_valid, error = validate_password(value)
    elif field == 'age':
        is_valid, error = validate_age(value)
    elif field == 'name':
        field_name = data.get('field_name', 'Name')
        is_valid, error = validate_name(value, field_name)
    else:
        return jsonify({
            "success": False,
            "error": f"Unknown field: {field}"
        }), 400

    return jsonify({
        "success": True,
        "field": field,
        "is_valid": is_valid,
        "error": error
    }), 200


@app.route('/api/validation-rules', methods=['GET'])
def validation_rules():
    """GET /api/validation-rules - Returns all validation rules"""
    return jsonify({
        "rules": {
            "username": {
                "description": "3-20 alphanumeric characters or underscore",
                "pattern": "^[a-zA-Z0-9_]{3,20}$",
                "example": "john_doe"
            },
            "email": {
                "description": "Valid email format",
                "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "example": "john@example.com"
            },
            "password": {
                "description": "8+ chars, uppercase, lowercase, digit, special char",
                "requirements": [
                    "At least 8 characters",
                    "At least 1 uppercase letter (A-Z)",
                    "At least 1 lowercase letter (a-z)",
                    "At least 1 digit (0-9)",
                    "At least 1 special character (!@#$%^&*)"
                ],
                "example": "SecurePass123!"
            },
            "age": {
                "description": "Integer between 13 and 120",
                "min": 13,
                "max": 120,
                "example": 28
            },
            "name": {
                "description": "2-50 letters, spaces, hyphens, apostrophes",
                "pattern": "^[a-zA-Z\\s\\'-]{2,50}$",
                "example": "John O'Brien-Smith"
            }
        }
    }), 200


if __name__ == '__main__':
    print("=" * 70)
    print("Flask Demo 5: Data Validation")
    print("=" * 70)
    print("\nValidation Examples:")
    print("\n1. Register with valid data:")
    print("   curl -X POST http://localhost:5000/api/register \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{")
    print("       \"username\":\"john_doe\",")
    print("       \"email\":\"john@example.com\",")
    print("       \"password\":\"SecurePass123!\",")
    print("       \"age\":28")
    print("     }'")
    print("\n2. Register with weak password:")
    print("   curl -X POST http://localhost:5000/api/register \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{")
    print("       \"username\":\"john_doe\",")
    print("       \"email\":\"john@example.com\",")
    print("       \"password\":\"123\",")
    print("       \"age\":28")
    print("     }'")
    print("\n3. Update profile:")
    print("   curl -X PUT http://localhost:5000/api/users/1/profile \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"age\":30,\"first_name\":\"Alice\"}'")
    print("\n4. Validate single field:")
    print("   curl -X POST http://localhost:5000/api/validate \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"field\":\"email\",\"value\":\"test@example.com\"}'")
    print("\n5. View validation rules:")
    print("   curl http://localhost:5000/api/validation-rules")
    print("\n" + "=" * 70)
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    app.run(debug=True, port=5000)
