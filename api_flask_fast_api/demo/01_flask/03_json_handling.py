"""
Flask Demo 3: JSON Request/Response Handling
Demonstrates receiving and returning JSON data with proper headers

Usage:
    python 03_json_handling.py

Testing:
    # Create article with JSON request
    curl -X POST http://localhost:5000/api/articles \
      -H "Content-Type: application/json" \
      -d '{"title":"Python Tips","content":"Learn Python","author":"Alice"}'

    # Retrieve articles
    curl http://localhost:5000/api/articles

    # Update article with JSON
    curl -X PUT http://localhost:5000/api/articles/1 \
      -H "Content-Type: application/json" \
      -d '{"title":"Updated Title","content":"New content","published":true}'

    # Search articles
    curl "http://localhost:5000/api/articles/search?q=Python"
"""

from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for articles
articles_db = {
    1: {
        "id": 1,
        "title": "Getting Started with Flask",
        "content": "Flask is a lightweight web framework for Python.",
        "author": "Alice",
        "created_at": "2024-01-15T10:30:00Z",
        "published": True,
        "tags": ["flask", "python", "web"],
    },
    2: {
        "id": 2,
        "title": "REST API Best Practices",
        "content": "Building scalable and maintainable REST APIs.",
        "author": "Bob",
        "created_at": "2024-02-20T14:45:00Z",
        "published": True,
        "tags": ["rest", "api", "best-practices"],
    },
}

next_article_id = 3


def get_current_timestamp():
    """Returns current timestamp in ISO 8601 format"""
    return datetime.utcnow().isoformat() + "Z"


@app.route("/api/articles", methods=["GET"])
def get_articles():
    """
    GET /api/articles
    Returns all articles as JSON
    """
    articles = list(articles_db.values())
    return jsonify({"success": True, "count": len(articles), "data": articles}), 200


@app.route("/api/articles/<int:article_id>", methods=["GET"])
def get_article(article_id):
    """
    GET /api/articles/:id
    Returns specific article by ID
    """
    if article_id not in articles_db:
        return jsonify(
            {"success": False, "error": "Article not found", "article_id": article_id}
        ), 404

    return jsonify({"success": True, "data": articles_db[article_id]}), 200


@app.route("/api/articles", methods=["POST"])
def create_article():
    """
    POST /api/articles
    Create new article from JSON request body

    Expected JSON format:
    {
        "title": "Article Title",
        "content": "Article content...",
        "author": "Author Name",
        "tags": ["tag1", "tag2"],
        "published": false
    }
    """
    global next_article_id

    # Check content-type
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Request must have Content-Type: application/json",
            }
        ), 400

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"success": False, "error": f"Invalid JSON: {str(e)}"}), 400

    # Validate required fields
    required_fields = ["title", "content", "author"]
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify(
            {
                "success": False,
                "error": "Missing required fields",
                "missing": missing_fields,
            }
        ), 400

    # Create article
    new_article = {
        "id": next_article_id,
        "title": data["title"],
        "content": data["content"],
        "author": data["author"],
        "created_at": get_current_timestamp(),
        "published": data.get("published", False),
        "tags": data.get("tags", []),
    }

    articles_db[next_article_id] = new_article
    next_article_id += 1

    return jsonify(
        {"success": True, "message": "Article created", "data": new_article}
    ), 201


@app.route("/api/articles/<int:article_id>", methods=["PUT"])
def update_article(article_id):
    """
    PUT /api/articles/:id
    Update existing article with JSON body
    """
    if article_id not in articles_db:
        return jsonify({"success": False, "error": "Article not found"}), 404

    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Request must have Content-Type: application/json",
            }
        ), 400

    data = request.get_json()

    # Update fields
    article = articles_db[article_id]
    if "title" in data:
        article["title"] = data["title"]
    if "content" in data:
        article["content"] = data["content"]
    if "author" in data:
        article["author"] = data["author"]
    if "published" in data:
        article["published"] = data["published"]
    if "tags" in data:
        article["tags"] = data["tags"]

    return jsonify(
        {"success": True, "message": "Article updated", "data": article}
    ), 200


@app.route("/api/articles/<int:article_id>", methods=["DELETE"])
def delete_article(article_id):
    """
    DELETE /api/articles/:id
    Remove article by ID
    """
    if article_id not in articles_db:
        return jsonify({"success": False, "error": "Article not found"}), 404

    deleted = articles_db.pop(article_id)

    return jsonify(
        {"success": True, "message": "Article deleted", "data": deleted}
    ), 200


@app.route("/api/articles/search", methods=["GET"])
def search_articles():
    """
    GET /api/articles/search?q=keyword
    Search articles by keyword
    """
    query = request.args.get("q", "").lower()

    if not query:
        return jsonify({"success": False, "error": "Search query is required"}), 400

    # Search in title, content, and tags
    results = []
    for article in articles_db.values():
        if (
            query in article["title"].lower()
            or query in article["content"].lower()
            or any(query in tag.lower() for tag in article["tags"])
        ):
            results.append(article)

    return jsonify(
        {"success": True, "query": query, "count": len(results), "data": results}
    ), 200


@app.route("/api/articles/stats", methods=["GET"])
def article_stats():
    """
    GET /api/articles/stats
    Returns statistics about articles
    """
    published_count = sum(1 for a in articles_db.values() if a["published"])
    draft_count = len(articles_db) - published_count
    authors = set(a["author"] for a in articles_db.values())

    return jsonify(
        {
            "success": True,
            "total_articles": len(articles_db),
            "published": published_count,
            "drafts": draft_count,
            "unique_authors": len(authors),
            "authors": list(authors),
        }
    ), 200


@app.route("/api/health", methods=["GET"])
def health():
    """GET /api/health - Server health check"""
    return jsonify(
        {
            "status": "healthy",
            "service": "JSON Handling Demo",
            "timestamp": get_current_timestamp(),
        }
    ), 200


@app.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify({"success": False, "error": "Bad request"}), 400


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == "__main__":
    print("=" * 70)
    print("Flask Demo 3: JSON Request/Response Handling")
    print("=" * 70)
    print("\nJSON Handling Examples:")
    print("\n1. GET - Retrieve all articles as JSON:")
    print("   curl http://localhost:5000/api/articles")
    print("\n2. GET - Retrieve specific article:")
    print("   curl http://localhost:5000/api/articles/1")
    print("\n3. POST - Create article with JSON body:")
    print("   curl -X POST http://localhost:5000/api/articles \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{")
    print('       "title":"My Article",')
    print('       "content":"Content here",')
    print('       "author":"Me",')
    print('       "tags":["python"],')
    print('       "published":true')
    print("     }'")
    print("\n4. PUT - Update article:")
    print("   curl -X PUT http://localhost:5000/api/articles/1 \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"published\":true}'")
    print("\n5. DELETE - Remove article:")
    print("   curl -X DELETE http://localhost:5000/api/articles/1")
    print("\n6. Search articles:")
    print("   curl 'http://localhost:5000/api/articles/search?q=Flask'")
    print("\n7. Statistics:")
    print("   curl http://localhost:5000/api/articles/stats")
    print("\n" + "=" * 70)
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    app.run(debug=True, port=5000)
