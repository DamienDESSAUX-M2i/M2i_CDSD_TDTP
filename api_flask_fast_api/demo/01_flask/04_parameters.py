"""
Flask Demo 4: URL Parameters and Query Strings
Demonstrates path parameters, query strings, and form data

Usage:
    python 04_parameters.py

Testing:
    # Path parameters
    curl http://localhost:5000/api/products/5
    curl http://localhost:5000/api/users/john/posts

    # Query strings
    curl "http://localhost:5000/api/products/search?category=electronics&min=100&max=1000"
    curl "http://localhost:5000/api/posts?page=2&limit=10&sort=date"

    # Combining path and query parameters
    curl "http://localhost:5000/api/users/alice/posts?status=published"

    # Form data (POST)
    curl -X POST http://localhost:5000/api/users \
      -d "name=Alice&age=30&city=Paris"
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample product database
products_db = {
    1: {"id": 1, "name": "Laptop", "category": "electronics", "price": 1200},
    2: {"id": 2, "name": "Phone", "category": "electronics", "price": 800},
    3: {"id": 3, "name": "Desk", "category": "furniture", "price": 300},
    4: {"id": 4, "name": "Chair", "category": "furniture", "price": 150},
    5: {"id": 5, "name": "Monitor", "category": "electronics", "price": 400}
}

# Sample posts database
posts_db = {
    1: {"id": 1, "user": "alice", "title": "Python Tips", "status": "published"},
    2: {"id": 2, "user": "alice", "title": "Flask Tutorial", "status": "draft"},
    3: {"id": 3, "user": "bob", "title": "Web Dev Basics", "status": "published"},
    4: {"id": 4, "user": "bob", "title": "REST APIs", "status": "published"},
}


# ============================================================================
# DEMO 1: Path Parameters
# ============================================================================

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    GET /api/products/:id
    Returns product by ID (path parameter)

    Example:
        curl http://localhost:5000/api/products/1
    """
    if product_id not in products_db:
        return jsonify({
            "success": False,
            "error": f"Product {product_id} not found"
        }), 404

    return jsonify({
        "success": True,
        "data": products_db[product_id]
    }), 200


@app.route('/api/users/<username>/posts', methods=['GET'])
def get_user_posts(username):
    """
    GET /api/users/:username/posts
    Returns all posts by a specific user (string path parameter)

    Example:
        curl http://localhost:5000/api/users/alice/posts
    """
    user_posts = [p for p in posts_db.values() if p['user'] == username.lower()]

    if not user_posts:
        return jsonify({
            "success": True,
            "username": username,
            "count": 0,
            "data": []
        }), 200

    return jsonify({
        "success": True,
        "username": username,
        "count": len(user_posts),
        "data": user_posts
    }), 200


@app.route('/api/users/<username>/posts/<int:post_id>', methods=['GET'])
def get_user_post(username, post_id):
    """
    GET /api/users/:username/posts/:id
    Returns specific post by user and post ID (multiple path parameters)

    Example:
        curl http://localhost:5000/api/users/alice/posts/1
    """
    if post_id not in posts_db:
        return jsonify({
            "success": False,
            "error": "Post not found"
        }), 404

    post = posts_db[post_id]
    if post['user'] != username.lower():
        return jsonify({
            "success": False,
            "error": "Post does not belong to this user"
        }), 404

    return jsonify({
        "success": True,
        "data": post
    }), 200


# ============================================================================
# DEMO 2: Query Strings
# ============================================================================

@app.route('/api/products/search', methods=['GET'])
def search_products():
    """
    GET /api/products/search?category=...&min=...&max=...
    Search products with query parameters

    Query Parameters:
        category (str): Filter by category
        min (int): Minimum price
        max (int): Maximum price
        limit (int): Max results (default: 10)

    Examples:
        curl "http://localhost:5000/api/products/search?category=electronics"
        curl "http://localhost:5000/api/products/search?min=100&max=1000"
        curl "http://localhost:5000/api/products/search?category=electronics&min=300&max=1200"
    """
    # Get query parameters with defaults
    category = request.args.get('category', None)
    try:
        min_price = int(request.args.get('min', 0))
        max_price = int(request.args.get('max', 999999))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({
            "success": False,
            "error": "min, max, and limit must be integers"
        }), 400

    # Filter products
    results = []
    for product in products_db.values():
        # Apply filters
        if category and product['category'] != category:
            continue
        if product['price'] < min_price or product['price'] > max_price:
            continue
        results.append(product)

    # Apply limit
    results = results[:limit]

    return jsonify({
        "success": True,
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "limit": limit
        },
        "count": len(results),
        "data": results
    }), 200


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    GET /api/posts?page=...&limit=...&sort=...&status=...
    Get posts with pagination and filtering

    Query Parameters:
        page (int): Page number (1-based, default: 1)
        limit (int): Items per page (default: 10)
        sort (str): Sort field - 'id', 'user', 'title' (default: 'id')
        status (str): Filter by status - 'published', 'draft'

    Examples:
        curl "http://localhost:5000/api/posts"
        curl "http://localhost:5000/api/posts?page=1&limit=2"
        curl "http://localhost:5000/api/posts?status=published"
        curl "http://localhost:5000/api/posts?sort=user"
    """
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({
            "success": False,
            "error": "page and limit must be integers"
        }), 400

    sort_by = request.args.get('sort', 'id')
    status = request.args.get('status', None)

    if page < 1:
        return jsonify({
            "success": False,
            "error": "page must be >= 1"
        }), 400

    # Filter by status
    results = list(posts_db.values())
    if status:
        results = [p for p in results if p['status'] == status]

    # Sort
    valid_sorts = ['id', 'user', 'title']
    if sort_by not in valid_sorts:
        return jsonify({
            "success": False,
            "error": f"sort must be one of: {', '.join(valid_sorts)}"
        }), 400

    results = sorted(results, key=lambda x: x[sort_by])

    # Paginate
    start = (page - 1) * limit
    end = start + limit
    paginated = results[start:end]

    return jsonify({
        "success": True,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_items": len(results),
            "total_pages": (len(results) + limit - 1) // limit
        },
        "filters": {
            "status": status,
            "sort": sort_by
        },
        "count": len(paginated),
        "data": paginated
    }), 200


# ============================================================================
# DEMO 3: Combining Path and Query Parameters
# ============================================================================

@app.route('/api/users/<username>/posts', methods=['GET'])
def get_user_posts_filtered(username):
    """
    GET /api/users/:username/posts?status=...
    Get user's posts with optional status filter

    Examples:
        curl "http://localhost:5000/api/users/alice/posts?status=published"
    """
    status = request.args.get('status', None)

    user_posts = [p for p in posts_db.values() if p['user'] == username.lower()]

    if status:
        user_posts = [p for p in user_posts if p['status'] == status]

    return jsonify({
        "success": True,
        "username": username,
        "filter": {"status": status},
        "count": len(user_posts),
        "data": user_posts
    }), 200


# ============================================================================
# DEMO 4: Form Data (POST)
# ============================================================================

@app.route('/api/register', methods=['POST'])
def register_user():
    """
    POST /api/register
    Register user with form data (application/x-www-form-urlencoded)

    Form Fields:
        name (str): User's name
        email (str): User's email
        age (int): User's age

    Examples:
        curl -X POST http://localhost:5000/api/register \
          -d "name=Alice&email=alice@example.com&age=30"
    """
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age')

    # Validate
    if not all([name, email, age]):
        return jsonify({
            "success": False,
            "error": "Missing required fields: name, email, age"
        }), 400

    try:
        age_int = int(age)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "age must be an integer"
        }), 400

    if age_int < 18:
        return jsonify({
            "success": False,
            "error": "Must be 18 or older"
        }), 400

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "data": {
            "name": name,
            "email": email,
            "age": age_int,
            "registered": True
        }
    }), 201


# ============================================================================
# DEMO 5: Mixed Parameters (path + query + form)
# ============================================================================

@app.route('/api/categories/<category>/products', methods=['GET'])
def get_category_products(category):
    """
    GET /api/categories/:category/products?min=...&max=...&sort=...
    Get products in category with price filtering

    Examples:
        curl "http://localhost:5000/api/categories/electronics/products"
        curl "http://localhost:5000/api/categories/electronics/products?min=300&max=1000"
    """
    try:
        min_price = int(request.args.get('min', 0))
        max_price = int(request.args.get('max', 999999))
    except ValueError:
        return jsonify({
            "success": False,
            "error": "min and max must be integers"
        }), 400

    # Filter by category and price
    results = [
        p for p in products_db.values()
        if p['category'] == category and min_price <= p['price'] <= max_price
    ]

    return jsonify({
        "success": True,
        "category": category,
        "filters": {
            "min_price": min_price,
            "max_price": max_price
        },
        "count": len(results),
        "data": results
    }), 200


@app.route('/api/demo', methods=['GET'])
def demo_info():
    """GET /api/demo - Shows all available parameter types"""
    return jsonify({
        "title": "Flask Parameter Handling Demo",
        "examples": {
            "path_parameters": [
                "GET /api/products/5",
                "GET /api/users/alice/posts",
                "GET /api/users/alice/posts/1"
            ],
            "query_strings": [
                "GET /api/products/search?category=electronics&min=100&max=1000",
                "GET /api/posts?page=2&limit=10&sort=user&status=published"
            ],
            "combined": [
                "GET /api/categories/electronics/products?min=300&max=1200"
            ],
            "form_data": [
                "POST /api/register with form fields"
            ]
        }
    }), 200


if __name__ == '__main__':
    print("=" * 70)
    print("Flask Demo 4: URL Parameters and Query Strings")
    print("=" * 70)
    print("\nParameter Types:")
    print("\n1. Path Parameters (in URL):")
    print("   curl http://localhost:5000/api/products/1")
    print("   curl http://localhost:5000/api/users/alice/posts")
    print("\n2. Query Strings (?key=value):")
    print("   curl 'http://localhost:5000/api/products/search?category=electronics'")
    print("   curl 'http://localhost:5000/api/posts?page=1&limit=5&status=published'")
    print("\n3. Combined Path + Query:")
    print("   curl 'http://localhost:5000/api/categories/electronics/products?min=300'")
    print("\n4. Form Data (POST):")
    print("   curl -X POST http://localhost:5000/api/register \\")
    print("     -d 'name=Alice&email=alice@example.com&age=30'")
    print("\n5. Info:")
    print("   curl http://localhost:5000/api/demo")
    print("\n" + "=" * 70)
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    app.run(debug=True, port=5000)
