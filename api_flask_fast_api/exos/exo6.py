from datetime import datetime
from typing import Dict, List, Optional

from flask import Flask, jsonify, request

app = Flask(__name__)


# ============================================================================
# Data Models
# ============================================================================


class Author:
    """Author model"""

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Post:
    """Post model"""

    def __init__(self, id: int, title: str, content: str, author_id: int):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# ============================================================================
# Repository Layer (Data Access)
# ============================================================================


class AuthorRepository:
    """
    Repository for Author data access
    Handles all database operations (CRUD)
    """

    def __init__(self):
        self.authors: Dict[int, Author] = {}
        self.next_id = 1
        self._initialize_data()

    def _initialize_data(self):
        """Initialize with sample data"""
        self.create(Author(1, "Author1"))
        self.create(Author(2, "Author2"))
        self.create(Author(3, "Author3"))
        self.create(Author(4, "Author4"))
        self.next_id = 5

    def create(self, author: Author) -> Author:
        """Create new author"""
        self.authors[author.id] = author
        return author

    def get_by_id(self, author_id: int) -> Optional[Author]:
        """Get author by ID"""
        return self.authors.get(author_id)

    def get_all(self) -> List[Author]:
        """Get all authors"""
        return list(self.authors.values())

    def update(self, author_id: int, **kwargs) -> Optional[Author]:
        """Update author"""
        if author_id not in self.authors:
            return None

        author = self.authors[author_id]
        for key, value in kwargs.items():
            if hasattr(author, key) and key not in ["id", "created_at"]:
                setattr(author, key, value)
        author.updated_at = datetime.now().isoformat()
        return author

    def delete(self, author_id: int) -> bool:
        """Delete author"""
        if author_id in self.authors:
            del self.authors[author_id]
            return True
        return False

    def find_by_name(self, name: str) -> List[Author]:
        """Find authors by name (case-insensitive)"""
        name_lower = name.lower()
        return [
            author
            for author in self.authors.values()
            if name_lower in author.name.lower()
        ]

    def get_next_id(self) -> int:
        """Get next available ID"""
        result = self.next_id
        self.next_id += 1
        return result


class PostRepository:
    """
    Repository for Post data access
    Handles all database operations (CRUD)
    """

    def __init__(self):
        self.posts: Dict[int, Post] = {}
        self.next_id = 1
        self._initialize_data()

    def _initialize_data(self):
        """Initialize with sample data"""
        self.create(Post(1, "Titre1", "Content1", 1))
        self.create(Post(2, "Titre2", "Content2", 1))
        self.create(Post(3, "Titre3", "Content3", 2))
        self.create(Post(4, "Titre4", "Content4", 4))
        self.next_id = 5

    def create(self, post: Post) -> Post:
        """Create new post"""
        self.posts[post.id] = post
        return post

    def get_by_id(self, post_id: int) -> Optional[Post]:
        """Get post by ID"""
        return self.posts.get(post_id)

    def get_all(self) -> List[Post]:
        """Get all posts"""
        return list(self.posts.values())

    def update(self, post_id: int, **kwargs) -> Optional[Post]:
        """Update post"""
        if post_id not in self.posts:
            return None

        post = self.posts[post_id]
        for key, value in kwargs.items():
            if hasattr(post, key) and key not in ["id", "created_at"]:
                setattr(post, key, value)
        post.updated_at = datetime.now().isoformat()
        return post

    def delete(self, post_id: int) -> bool:
        """Delete post"""
        if post_id in self.posts:
            del self.posts[post_id]
            return True
        return False

    def find_by_author_id(self, author_id: str) -> List[Post]:
        """Find posts by author_id"""
        return [post for post in self.posts.values() if author_id == post.author_id]

    def get_next_id(self) -> int:
        """Get next available ID"""
        result = self.next_id
        self.next_id += 1
        return result


# ============================================================================
# Service Layer (Business Logic)
# ============================================================================


class Service:
    """
    Author and Post service - handles business logic
    Implements CRUD operations and business rules
    """

    def __init__(
        self, author_repository: AuthorRepository, post_repository: PostRepository
    ):
        self.author_repository = author_repository
        self.post_repository = post_repository

    def get_all_authors(self) -> List[dict]:
        """Get all authors"""
        authors = self.author_repository.get_all()
        return [author.to_dict() for author in authors]

    def get_author(self, author_id: int) -> Optional[dict]:
        """Get author by ID"""
        author = self.author_repository.get_by_id(author_id)
        return author.to_dict() if author else None

    def create_author(self, name: str) -> dict:
        """
        Create new author with validation

        Raises:
            ValueError: If validation fails
        """
        if not name or len(name) < 1:
            raise ValueError("author name must be at least 1 characters")

        authors = self.author_repository.get_all()
        if any(name == author.name for author in authors):
            raise ValueError(f"Author name {name} already exists")

        author_id = self.author_repository.get_next_id()
        author = Author(author_id, name)
        self.author_repository.create(author)

        return author.to_dict()

    def update_author(self, author_id: int, **kwargs) -> Optional[dict]:
        """
        Update author with validation

        Raises:
            ValueError: If validation fails
        """
        author = self.author_repository.get_by_id(author_id)
        if not author:
            return None

        if "name" in kwargs:
            if not kwargs["name"] or len(kwargs["name"]) < 1:
                raise ValueError("author name must be at least 1 characters")

            authors = self.author_repository.get_all()
            name = kwargs["name"]
            if any(name == author.name for author in authors):
                raise ValueError(f"Author name {name} already exists")

        updated = self.author_repository.update(author_id, **kwargs)
        return updated.to_dict() if updated else None

    def delete_author(self, author_id: int) -> bool:
        """Delete author"""
        return self.author_repository.delete(author_id)

    def search_authors(self, name: str) -> list[dict]:
        """Search author by name"""
        results = self.author_repository.get_all()
        results = [author for author in results if name.lower() in author.name.lower()]
        return [author.to_dict() for author in results]

    def get_all_posts(self) -> List[dict]:
        """Get all posts"""
        posts = self.post_repository.get_all()
        return [post.to_dict() for post in posts]

    def get_post(self, post_id: int) -> Optional[dict]:
        """Get post by ID"""
        post = self.post_repository.get_by_id(post_id)
        return post.to_dict() if post else None

    def create_post(self, title: str, content: str, author_name: str) -> dict:
        """Create post using author name"""
        if not title or len(title) < 1:
            raise ValueError("post title must be at least 1 character")

        if not content or len(content) < 1:
            raise ValueError("post content must be at least 1 character")

        if not author_name or len(author_name) < 1:
            raise ValueError("author name must be provided")

        authors = self.author_repository.get_all()
        author = next((a for a in authors if a.name == author_name), None)

        if not author:
            raise ValueError(f"Author '{author_name}' does not exist")

        post_id = self.post_repository.get_next_id()
        post = Post(post_id, title, content, author.id)
        self.post_repository.create(post)

        return post.to_dict()

    def update_post(self, post_id: int, **kwargs) -> Optional[dict]:
        """
        Update post with validation

        Raises:
            ValueError: If validation fails
        """
        post = self.post_repository.get_by_id(post_id)
        if not post:
            return None

        if "title" in kwargs:
            if not kwargs["title"] or len(kwargs["title"]) < 1:
                raise ValueError("post title must be at least 1 character")

        if "content" in kwargs:
            if not kwargs["content"] or len(kwargs["content"]) < 1:
                raise ValueError("post content must be at least 1 character")

        updated = self.post_repository.update(post_id, **kwargs)
        return updated.to_dict() if updated else None

    def delete_post(self, post_id: int) -> bool:
        """Delete post"""
        return self.post_repository.delete(post_id)

    def get_posts_by_author(self, author_id: int) -> List[dict]:
        """Get posts by author ID"""
        posts = self.post_repository.find_by_author_id(author_id)
        return [post.to_dict() for post in posts]

    def search_posts(self, query: str) -> List[dict]:
        """Search posts by title or content"""
        posts = self.post_repository.get_all()
        results = [
            post
            for post in posts
            if query.lower() in post.title.lower()
            or query.lower() in post.content.lower()
        ]
        return [post.to_dict() for post in results]


# ============================================================================
# Initialize Layers
# ============================================================================

author_repository = AuthorRepository()
post_repository = PostRepository()
service = Service(author_repository, post_repository)


# ============================================================================
# Controller Layer (Flask Routes)
# ============================================================================


@app.route("/api/post", methods=["GET"])
def get_all_post():
    """GET /api/post - Get all post"""
    try:
        post = service.get_all_posts()
        return jsonify({"success": True, "count": len(post), "data": post}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/post/<int:post_id>", methods=["GET"])
def get_post(post_id):
    """GET /api/post/:id - Get specific post"""
    try:
        post = service.get_post(post_id)
        if not post:
            return jsonify(
                {"success": False, "error": f"post {post_id} not found"}
            ), 404

        return jsonify({"success": True, "data": post}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/post", methods=["POST"])
def create_post():
    """POST /api/post - Create new post"""
    try:
        if not request.is_json:
            return jsonify(
                {"success": False, "error": "Content-Type must be application/json"}
            ), 400

        data = request.get_json()
        required = ["title", "content", "author_name"]
        if not all(f in data for f in required):
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing required fields: {', '.join(required)}",
                }
            ), 400

        post = service.create_post(
            title=data["title"],
            content=data["content"],
            author_name=data["author_name"],
        )

        return jsonify({"success": True, "message": "post created", "data": post}), 201

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/post/<int:post_id>", methods=["PUT"])
def update_post_route(post_id):
    """PUT /api/post/:id - Update post"""
    try:
        if not request.is_json:
            return jsonify(
                {"success": False, "error": "Content-Type must be application/json"}
            ), 400

        data = request.get_json()
        kwargs = {}

        if "title" in data:
            kwargs["title"] = data["title"]
        if "content" in data:
            kwargs["content"] = float(data["content"])

        post = service.update_post(post_id, **kwargs)
        if not post:
            return jsonify(
                {"success": False, "error": f"post {post_id} not found"}
            ), 404

        return jsonify({"success": True, "message": "post updated", "data": post}), 200

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/post/<int:post_id>", methods=["DELETE"])
def delete_post_route(post_id):
    """DELETE /api/post/:id - Delete post"""
    try:
        if not service.delete_post(post_id):
            return jsonify(
                {"success": False, "error": f"post {post_id} not found"}
            ), 404

        return jsonify({"success": True, "message": "post deleted"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/post/search", methods=["GET"])
def search_post_route():
    """GET /api/post/search?query=..."""
    try:
        query = request.args.get("query")

        results = service.search_posts(query)

        return jsonify(
            {
                "success": True,
                "filters": {"query": query},
                "count": len(results),
                "data": results,
            }
        ), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/inventory/stats", methods=["GET"])
def inventory_stats():
    """GET /api/inventory/stats - Get inventory statistics"""
    try:
        posts = service.get_all_posts()
        authors = service.get_all_authors()

        return jsonify(
            {
                "success": True,
                "stats": {
                    "total_posts": len(posts),
                    "total_authors": len(authors),
                },
            }
        ), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
