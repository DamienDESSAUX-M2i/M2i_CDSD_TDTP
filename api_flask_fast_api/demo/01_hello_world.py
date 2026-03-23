"""
Flask Demo 1: Hello World
Simple Flask app with a single endpoint

Usage:
    python 01_hello_world.py
    # Server runs on http://localhost:5000

Testing:
    curl http://localhost:5000/
    curl http://localhost:5000/api/hello
    curl http://localhost:5000/api/hello?name=World
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    """Home endpoint - returns simple text"""
    return "Welcome to Flask Demo 1!"


@app.route("/api/hello", methods=["GET"])
def hello():
    """
    Hello endpoint with optional name parameter

    Args:
        name (str, optional): Name to greet. Defaults to "World"

    Returns:
        dict: JSON response with greeting

    Examples:
        GET /api/hello → {"message": "Hello, World!"}
        GET /api/hello?name=Alice → {"message": "Hello, Alice!"}
    """
    name = request.args.get("name", "World")
    return jsonify({"message": f"Hello, {name}!", "status": "success"})


@app.route("/api/info", methods=["GET"])
def info():
    """Returns server information"""
    return jsonify(
        {
            "app": "Flask Demo 1",
            "version": "1.0.0",
            "environment": "development",
            "endpoints": [
                "GET /",
                "GET /api/hello",
                "GET /api/hello?name=YourName",
                "GET /api/info",
            ],
        }
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    print("=" * 60)
    print("Flask Demo 1: Hello World")
    print("=" * 60)
    print("Server running on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET /")
    print("  GET /api/hello")
    print("  GET /api/hello?name=YourName")
    print("  GET /api/info")
    print("\nTest with curl:")
    print("  curl http://localhost:5000/api/hello")
    print("  curl 'http://localhost:5000/api/hello?name=Alice'")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")

    app.run(debug=True, port=5000)
