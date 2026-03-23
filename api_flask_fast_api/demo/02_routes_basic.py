"""
Flask Demo 2: Basic Routes (GET, POST, PUT, DELETE)
Demonstrates all HTTP methods with resource-based routing

Usage:
    python 02_routes_basic.py

Testing:
    # GET - retrieve all users
    curl http://localhost:5000/api/users

    # GET - retrieve specific user
    curl http://localhost:5000/api/users/1

    # POST - create new user
    curl -X POST http://localhost:5000/api/users \
      -H "Content-Type: application/json" \
      -d '{"name":"Alice","email":"alice@example.com"}'

    # PUT - update user
    curl -X PUT http://localhost:5000/api/users/1 \
      -H "Content-Type: application/json" \
      -d '{"name":"Alice Updated","email":"alice.new@example.com"}'

    # DELETE - remove user
    curl -X DELETE http://localhost:5000/api/users/1
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for users
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
    3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
}

next_user_id = 4


@app.route("/api/users", methods=["GET"])
def get_all_users():
    """
    GET /api/users
    Returns list of all users
    """
    return jsonify(
        {"success": True, "data": list(users_db.values()), "count": len(users_db)}
    ), 200


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    GET /api/users/:id
    Returns specific user by ID
    """
    if user_id not in users_db:
        return jsonify({"success": False, "error": f"User {user_id} not found"}), 404

    return jsonify({"success": True, "data": users_db[user_id]}), 200


@app.route("/api/users", methods=["POST"])
def create_user():
    """
    POST /api/users
    Create new user with JSON body: {"name": "...", "email": "..."}
    """
    global next_user_id

    # Validate JSON
    if not request.is_json:
        return jsonify(
            {"success": False, "error": "Content-Type must be application/json"}
        ), 400

    data = request.get_json()

    # Validate required fields
    if not data.get("name") or not data.get("email"):
        return jsonify(
            {"success": False, "error": "Missing required fields: name, email"}
        ), 400

    # Check for duplicate email
    for user in users_db.values():
        if user["email"] == data["email"]:
            return jsonify(
                {"success": False, "error": f"Email {data['email']} already exists"}
            ), 409

    # Create new user
    new_user = {"id": next_user_id, "name": data["name"], "email": data["email"]}
    users_db[next_user_id] = new_user
    next_user_id += 1

    return jsonify(
        {"success": True, "message": "User created successfully", "data": new_user}
    ), 201


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    PUT /api/users/:id
    Update existing user with JSON body: {"name": "...", "email": "..."}
    """
    if user_id not in users_db:
        return jsonify({"success": False, "error": f"User {user_id} not found"}), 404

    if not request.is_json:
        return jsonify(
            {"success": False, "error": "Content-Type must be application/json"}
        ), 400

    data = request.get_json()

    # Update fields if provided
    if "name" in data:
        users_db[user_id]["name"] = data["name"]
    if "email" in data:
        # Check if new email is already used by another user
        for uid, user in users_db.items():
            if uid != user_id and user["email"] == data["email"]:
                return jsonify(
                    {"success": False, "error": f"Email {data['email']} already in use"}
                ), 409
        users_db[user_id]["email"] = data["email"]

    return jsonify(
        {
            "success": True,
            "message": "User updated successfully",
            "data": users_db[user_id],
        }
    ), 200


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    DELETE /api/users/:id
    Remove user by ID
    """
    if user_id not in users_db:
        return jsonify({"success": False, "error": f"User {user_id} not found"}), 404

    deleted_user = users_db.pop(user_id)

    return jsonify(
        {"success": True, "message": "User deleted successfully", "data": deleted_user}
    ), 200


@app.route("/api/stats", methods=["GET"])
def stats():
    """GET /api/stats - Returns API statistics"""
    return jsonify(
        {
            "total_users": len(users_db),
            "next_id": next_user_id,
            "endpoints": {
                "GET": ["/api/users", "/api/users/<id>", "/api/stats"],
                "POST": ["/api/users"],
                "PUT": ["/api/users/<id>"],
                "DELETE": ["/api/users/<id>"],
            },
        }
    ), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == "__main__":
    print("=" * 70)
    print("Flask Demo 2: Basic Routes (GET, POST, PUT, DELETE)")
    print("=" * 70)
    print("\nHTTP Methods Demonstration:")
    print("\n1. GET - Retrieve Resources:")
    print("   curl http://localhost:5000/api/users")
    print("   curl http://localhost:5000/api/users/1")
    print("\n2. POST - Create Resource:")
    print("   curl -X POST http://localhost:5000/api/users \\")
    print("     -H 'Content-Type: application/json' \\")
    print('     -d \'{"name":"Alice","email":"alice@example.com"}\'')
    print("\n3. PUT - Update Resource:")
    print("   curl -X PUT http://localhost:5000/api/users/1 \\")
    print("     -H 'Content-Type: application/json' \\")
    print('     -d \'{"name":"Alice Updated"}\'')
    print("\n4. DELETE - Remove Resource:")
    print("   curl -X DELETE http://localhost:5000/api/users/1")
    print("\n5. Stats:")
    print("   curl http://localhost:5000/api/stats")
    print("\n" + "=" * 70)
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    app.run(debug=True, port=5000)
