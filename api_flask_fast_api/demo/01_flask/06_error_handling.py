"""
Flask Demo 6: Error Handling and HTTP Status Codes
Demonstrates proper error handling, custom exceptions, and HTTP status codes

Usage:
    python 06_error_handling.py

Testing:
    # Valid request
    curl http://localhost:5000/api/books/1

    # Resource not found
    curl http://localhost:5000/api/books/999

    # Invalid request (missing required fields)
    curl -X POST http://localhost:5000/api/books \
      -H "Content-Type: application/json" \
      -d '{}'

    # Invalid data type
    curl -X POST http://localhost:5000/api/books \
      -H "Content-Type: application/json" \
      -d '{"title":"Book","isbn":"invalid","pages":"not_a_number"}'

    # Access denied
    curl http://localhost:5000/api/admin/stats

    # Method not allowed
    curl -X DELETE http://localhost:5000/api/books/1
"""

from flask import Flask, request, jsonify
from enum import Enum

app = Flask(__name__)

# In-memory database
books_db = {
    1: {
        "id": 1,
        "title": "Python Basics",
        "author": "Alice",
        "isbn": "978-0-123456-78-9",
        "pages": 350,
        "published": 2022
    },
    2: {
        "id": 2,
        "title": "Web Development",
        "author": "Bob",
        "isbn": "978-0-987654-32-1",
        "pages": 450,
        "published": 2023
    }
}

next_book_id = 3


# ============================================================================
# Custom Exceptions
# ============================================================================

class APIException(Exception):
    """Base exception for API errors"""
    def __init__(self, message, status_code=500, details=None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(APIException):
    """Raised when data validation fails"""
    def __init__(self, message, field=None, details=None):
        super().__init__(message, 400, details)
        self.field = field


class ResourceNotFoundError(APIException):
    """Raised when resource is not found"""
    def __init__(self, resource_type, resource_id):
        message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(message, 404)
        self.resource_type = resource_type
        self.resource_id = resource_id


class ResourceAlreadyExistsError(APIException):
    """Raised when trying to create duplicate resource"""
    def __init__(self, message, field=None):
        super().__init__(message, 409)
        self.field = field


class AccessDeniedError(APIException):
    """Raised when user doesn't have permission"""
    def __init__(self, message="Access denied"):
        super().__init__(message, 403)


class AuthenticationError(APIException):
    """Raised when authentication fails"""
    def __init__(self, message="Authentication required"):
        super().__init__(message, 401)


# ============================================================================
# Validation
# ============================================================================

def validate_book_data(data):
    """
    Validate book data

    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(data, dict):
        raise ValidationError("Request body must be JSON object")

    # Required fields
    required = ['title', 'author', 'isbn', 'pages', 'published']
    missing = [f for f in required if f not in data]
    if missing:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing)}",
            details={"missing_fields": missing}
        )

    # Validate title
    if not isinstance(data['title'], str) or len(data['title']) < 1:
        raise ValidationError("Title must be non-empty string", field='title')

    if len(data['title']) > 200:
        raise ValidationError("Title too long (max 200 characters)", field='title')

    # Validate author
    if not isinstance(data['author'], str) or len(data['author']) < 1:
        raise ValidationError("Author must be non-empty string", field='author')

    # Validate ISBN format (simplified: XXX-X-XXXXXX-XX-X)
    isbn = str(data['isbn']).replace('-', '')
    if not isbn.isdigit() or len(isbn) != 10 and len(isbn) != 13:
        raise ValidationError(
            "ISBN must be 10 or 13 digits (format: XXX-X-XXXXXX-XX-X)",
            field='isbn'
        )

    # Validate pages
    try:
        pages = int(data['pages'])
        if pages < 1 or pages > 10000:
            raise ValueError()
    except (ValueError, TypeError):
        raise ValidationError(
            "Pages must be integer between 1 and 10000",
            field='pages'
        )

    # Validate published year
    try:
        year = int(data['published'])
        if year < 1000 or year > 2100:
            raise ValueError()
    except (ValueError, TypeError):
        raise ValidationError(
            "Published year must be integer between 1000 and 2100",
            field='published'
        )

    return True


def check_isbn_exists(isbn, exclude_id=None):
    """Check if ISBN already exists"""
    for book in books_db.values():
        if book['isbn'] == isbn and book['id'] != exclude_id:
            return True
    return False


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(APIException)
def handle_api_exception(error):
    """Handle custom API exceptions"""
    response = {
        "success": False,
        "error": error.message,
        "status_code": error.status_code
    }

    if hasattr(error, 'field') and error.field:
        response["field"] = error.field

    if error.details:
        response.update(error.details)

    return jsonify(response), error.status_code


@app.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify({
        "success": False,
        "error": "Bad request",
        "status_code": 400
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify({
        "success": False,
        "error": "Method not allowed",
        "allowed_methods": error.valid_methods if hasattr(error, 'valid_methods') else [],
        "status_code": 405
    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors"""
    print(f"Internal Server Error: {error}")
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "status_code": 500,
        "message": "Something went wrong on the server"
    }), 500


# ============================================================================
# Endpoints
# ============================================================================

@app.route('/api/books', methods=['GET'])
def get_books():
    """GET /api/books - Retrieve all books"""
    books = list(books_db.values())
    return jsonify({
        "success": True,
        "count": len(books),
        "data": books
    }), 200


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """GET /api/books/:id - Retrieve specific book"""
    if book_id not in books_db:
        raise ResourceNotFoundError("Book", book_id)

    return jsonify({
        "success": True,
        "data": books_db[book_id]
    }), 200


@app.route('/api/books', methods=['POST'])
def create_book():
    """
    POST /api/books
    Create new book with validation

    Returns:
        201: Book created
        400: Validation error
        409: ISBN already exists
    """
    global next_book_id

    # Check content-type
    if not request.is_json:
        raise ValidationError("Content-Type must be application/json")

    data = request.get_json()

    # Validate book data
    try:
        validate_book_data(data)
    except ValidationError:
        raise

    # Check ISBN doesn't exist
    if check_isbn_exists(data['isbn']):
        raise ResourceAlreadyExistsError(
            f"ISBN {data['isbn']} already exists",
            field='isbn'
        )

    # Create book
    new_book = {
        "id": next_book_id,
        "title": data['title'],
        "author": data['author'],
        "isbn": data['isbn'],
        "pages": int(data['pages']),
        "published": int(data['published'])
    }

    books_db[next_book_id] = new_book
    next_book_id += 1

    return jsonify({
        "success": True,
        "message": "Book created",
        "data": new_book
    }), 201


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    PUT /api/books/:id
    Update book with validation

    Returns:
        200: Book updated
        404: Book not found
        400: Validation error
    """
    if book_id not in books_db:
        raise ResourceNotFoundError("Book", book_id)

    if not request.is_json:
        raise ValidationError("Content-Type must be application/json")

    data = request.get_json()
    book = books_db[book_id]

    # Validate and update fields
    if 'title' in data:
        if not isinstance(data['title'], str) or len(data['title']) < 1:
            raise ValidationError("Title must be non-empty string", field='title')
        book['title'] = data['title']

    if 'author' in data:
        if not isinstance(data['author'], str) or len(data['author']) < 1:
            raise ValidationError("Author must be non-empty string", field='author')
        book['author'] = data['author']

    if 'isbn' in data:
        isbn = str(data['isbn']).replace('-', '')
        if not isbn.isdigit() or len(isbn) != 10 and len(isbn) != 13:
            raise ValidationError("Invalid ISBN format", field='isbn')
        if check_isbn_exists(data['isbn'], exclude_id=book_id):
            raise ResourceAlreadyExistsError("ISBN already exists", field='isbn')
        book['isbn'] = data['isbn']

    if 'pages' in data:
        try:
            pages = int(data['pages'])
            if pages < 1 or pages > 10000:
                raise ValueError()
            book['pages'] = pages
        except (ValueError, TypeError):
            raise ValidationError("Pages must be integer 1-10000", field='pages')

    if 'published' in data:
        try:
            year = int(data['published'])
            if year < 1000 or year > 2100:
                raise ValueError()
            book['published'] = year
        except (ValueError, TypeError):
            raise ValidationError("Published year must be 1000-2100", field='published')

    return jsonify({
        "success": True,
        "message": "Book updated",
        "data": book
    }), 200


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    DELETE /api/books/:id
    Delete book - requires admin role (simulated)
    """
    # Simulate permission check
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer admin'):
        raise AccessDeniedError("Admin role required to delete books")

    if book_id not in books_db:
        raise ResourceNotFoundError("Book", book_id)

    deleted = books_db.pop(book_id)

    return jsonify({
        "success": True,
        "message": "Book deleted",
        "data": deleted
    }), 200


@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    """GET /api/admin/stats - Admin-only endpoint"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer admin'):
        raise AccessDeniedError("Admin role required")

    return jsonify({
        "success": True,
        "stats": {
            "total_books": len(books_db),
            "next_id": next_book_id
        }
    }), 200


@app.route('/api/login', methods=['POST'])
def login():
    """
    POST /api/login
    Simulate login (missing credentials)
    """
    if not request.is_json:
        raise ValidationError("Content-Type must be application/json")

    data = request.get_json()

    # Validate credentials
    if 'username' not in data or 'password' not in data:
        raise AuthenticationError("Username and password required")

    # Simulate wrong credentials
    if data['username'] != 'admin' or data['password'] != 'secret':
        raise AuthenticationError("Invalid credentials")

    return jsonify({
        "success": True,
        "token": "Bearer admin",
        "message": "Login successful"
    }), 200


@app.route('/api/error-demo', methods=['GET'])
def error_demo():
    """GET /api/error-demo - Demonstrates error handling"""
    error_type = request.args.get('type', 'none')

    if error_type == 'not_found':
        raise ResourceNotFoundError("Item", 999)
    elif error_type == 'validation':
        raise ValidationError("Invalid input", field='email')
    elif error_type == 'access_denied':
        raise AccessDeniedError("You don't have permission")
    elif error_type == 'auth':
        raise AuthenticationError()
    elif error_type == 'exists':
        raise ResourceAlreadyExistsError("Email already registered", field='email')
    elif error_type == 'server':
        raise Exception("Simulated server error")
    else:
        return jsonify({
            "success": True,
            "message": "No error triggered",
            "available_errors": [
                "?type=not_found",
                "?type=validation",
                "?type=access_denied",
                "?type=auth",
                "?type=exists",
                "?type=server"
            ]
        }), 200


if __name__ == '__main__':
    print("=" * 70)
    print("Flask Demo 6: Error Handling and HTTP Status Codes")
    print("=" * 70)
    print("\nError Handling Examples:")
    print("\n1. Valid request (200):")
    print("   curl http://localhost:5000/api/books/1")
    print("\n2. Not found (404):")
    print("   curl http://localhost:5000/api/books/999")
    print("\n3. Validation error (400):")
    print("   curl -X POST http://localhost:5000/api/books \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{}'")
    print("\n4. Invalid ISBN (400):")
    print("   curl -X POST http://localhost:5000/api/books \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"title\":\"Book\",\"author\":\"X\",\"isbn\":\"123\",\"pages\":100,\"published\":2024}'")
    print("\n5. Access denied (403):")
    print("   curl http://localhost:5000/api/admin/stats")
    print("\n6. Demo errors:")
    print("   curl 'http://localhost:5000/api/error-demo?type=not_found'")
    print("   curl 'http://localhost:5000/api/error-demo?type=validation'")
    print("\n7. Login (401):")
    print("   curl -X POST http://localhost:5000/api/login \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"username\":\"admin\",\"password\":\"wrong\"}'")
    print("\n" + "=" * 70)
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    app.run(debug=True, port=5000)
