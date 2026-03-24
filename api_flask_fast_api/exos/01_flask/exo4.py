import re

from flask import Flask, jsonify, request

app = Flask(__name__)


users_db = {
    1: {
        "id": 1,
        "username": "john",
        "email": "john@example.com",
        "password": "secure123",
        "age": 25,
    },
}

next_user_id = 2


EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
USERNAME_PATTERN = r"^[a-zA-Z0-9_]{2,20}$"


def validate_username(username):
    """
    Validate username (alphanumeric + underscore, 2-20 chars)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not username or not isinstance(username, str):
        return False, "Username is required and must be a string"

    username = username.strip()
    if not re.match(USERNAME_PATTERN, username):
        return False, "Username must be 2-20 characters (letters, numbers, underscore)"

    return True, None


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

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least 1 uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least 1 lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least 1 digit"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least 1 special character"

    return True, None


def validate_age(age):
    """
    Validate age (must be integer between 18 and 100)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if age is None:
        return False, "Age is required"

    try:
        age_int = int(age)
    except (ValueError, TypeError):
        return False, "Age must be an integer"

    if age_int < 18:
        return False, "Must be at least 18 years old"

    if age_int > 100:
        return False, "Age cannot exceed 100"

    return True, None


def check_email_exists(email, exclude_id=None):
    """Check if email already exists"""
    for user in users_db.values():
        if user["email"].lower() == email.lower() and user["id"] != exclude_id:
            return True
    return False


@app.route("/register", methods=["POST"])
def create_user():
    global next_user_id

    if not request.is_json:
        return jsonify(
            {"success": False, "error": "Content-Type must be application/json"}
        ), 400

    data = request.get_json()
    required = ["username", "email", "password", "age"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify(
            {
                "success": False,
                "error": "Missing required fields",
                "missing_fields": missing,
            }
        ), 400

    is_valid, error = validate_username(data["username"])
    if not is_valid:
        return jsonify({"success": False, "field": "username", "error": error}), 400

    is_valid, error = validate_email(data["email"])
    if not is_valid:
        return jsonify({"success": False, "field": "email", "error": error}), 400

    if check_email_exists(data["email"]):
        return jsonify(
            {"success": False, "field": "email", "error": "Email already registered"}
        ), 409

    is_valid, error = validate_password(data["password"])
    if not is_valid:
        return jsonify({"success": False, "field": "password", "error": error}), 400

    is_valid, error = validate_age(data["age"])
    if not is_valid:
        return jsonify({"success": False, "field": "age", "error": error}), 400

    new_user = {
        "id": next_user_id,
        "username": data["username"],
        "email": data["email"],
        "password": data["password"],
        "age": data["age"],
    }
    users_db[next_user_id] = new_user
    next_user_id += 1

    return jsonify(
        {"success": True, "message": "Registration successful", "user": new_user}
    ), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
