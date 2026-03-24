"""
FastAPI Demo 2: Pydantic Models
Demonstrates automatic validation with Pydantic models

Pydantic Features:
    - Automatic type validation
    - JSON serialization/deserialization
    - Documentation in API docs
    - Error messages with field details
    - Support for complex types (datetime, UUID, etc)

Usage:
    python 02_pydantic_models.py

Testing:
    # Create user (valid)
    curl -X POST http://localhost:8000/api/users \
      -H "Content-Type: application/json" \
      -d '{"name":"Alice","email":"alice@example.com","age":28}'

    # Create user (invalid - missing field)
    curl -X POST http://localhost:8000/api/users \
      -H "Content-Type: application/json" \
      -d '{"name":"Alice","age":28}'

    # Create product (valid with optional fields)
    curl -X POST http://localhost:8000/api/products \
      -H "Content-Type: application/json" \
      -d '{"name":"Laptop","price":1200.99}'
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="FastAPI Pydantic Models Demo",
    description="Demonstrates automatic validation with Pydantic models",
    version="1.0.0"
)


# ============================================================================
# Pydantic Models
# ============================================================================

class User(BaseModel):
    """User model with validation"""
    name: str = Field(..., min_length=2, max_length=50, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    age: int = Field(..., ge=18, le=120, description="User's age (18-120)")
    is_active: bool = Field(default=True, description="Is user active?")

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "age": 28,
                "is_active": True
            }
        }


class Product(BaseModel):
    """Product model with optional fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    price: float = Field(..., gt=0, description="Product price (must be > 0)")
    stock: int = Field(default=0, ge=0, description="Available stock")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    is_available: bool = Field(default=True, description="Is product available?")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop Pro",
                "price": 1299.99,
                "stock": 10,
                "description": "High-performance laptop",
                "is_available": True
            }
        }


class Article(BaseModel):
    """Article model with nested field"""
    title: str = Field(..., min_length=5, max_length=200, description="Article title")
    content: str = Field(..., min_length=10, description="Article content")
    author: str = Field(..., min_length=2, description="Author name")
    tags: List[str] = Field(default_factory=list, description="Article tags")
    published: bool = Field(default=False, description="Is published?")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Getting Started with FastAPI",
                "content": "FastAPI is a modern web framework...",
                "author": "John Doe",
                "tags": ["fastapi", "python", "api"],
                "published": True
            }
        }


class UserResponse(BaseModel):
    """Response model for user (without sensitive fields)"""
    id: int
    name: str
    email: str
    is_active: bool
    created_at: str


class ProductUpdate(BaseModel):
    """Partial update model (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)
    is_available: Optional[bool] = None


# ============================================================================
# In-memory storage
# ============================================================================

users_db = {
    1: {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "age": 28,
        "is_active": True,
        "created_at": "2024-01-15T10:30:00Z"
    }
}

products_db = {
    1: {
        "id": 1,
        "name": "Laptop Pro",
        "price": 1299.99,
        "stock": 10,
        "description": "High-performance laptop",
        "is_available": True
    }
}

articles_db = {
    1: {
        "id": 1,
        "title": "Getting Started with FastAPI",
        "content": "FastAPI is a modern web framework for building APIs...",
        "author": "John Doe",
        "tags": ["fastapi", "python"],
        "published": True,
        "created_at": "2024-01-15T10:30:00Z"
    }
}

next_user_id = 2
next_product_id = 2
next_article_id = 2


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
def root():
    """Root endpoint"""
    return {"message": "FastAPI Pydantic Models Demo"}


@app.post("/api/users", response_model=UserResponse, status_code=201, tags=["Users"])
def create_user(user: User):
    """
    Create new user with automatic validation

    FastAPI automatically:
    - Validates type hints
    - Validates Pydantic constraints (email format, age range)
    - Returns error 422 with field validation details
    - Generates documentation in Swagger UI
    """
    global next_user_id

    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "is_active": user.is_active,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    users_db[next_user_id] = new_user
    next_user_id += 1

    return new_user


@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int):
    """Get user by ID"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return users_db[user_id]


@app.post("/api/products", status_code=201, tags=["Products"])
def create_product(product: Product):
    """
    Create new product

    Pydantic validation rules:
    - name: 1-100 characters
    - price: must be > 0
    - stock: must be >= 0 (optional, default 0)
    - description: optional, max 500 chars
    """
    global next_product_id

    new_product = {
        "id": next_product_id,
        **product.dict()
    }

    products_db[next_product_id] = new_product
    next_product_id += 1

    return {
        "success": True,
        "message": "Product created",
        "data": new_product
    }


@app.get("/api/products/{product_id}", tags=["Products"])
def get_product(product_id: int):
    """Get product by ID"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return products_db[product_id]


@app.put("/api/products/{product_id}", tags=["Products"])
def update_product(product_id: int, product: ProductUpdate):
    """
    Update product (partial update)

    All fields are optional. Only provided fields are updated.
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    # Update only provided fields
    update_data = product.dict(exclude_unset=True)
    existing_product = products_db[product_id]
    updated_product = {**existing_product, **update_data}

    products_db[product_id] = updated_product

    return {
        "success": True,
        "message": "Product updated",
        "data": updated_product
    }


@app.post("/api/articles", status_code=201, tags=["Articles"])
def create_article(article: Article):
    """
    Create new article

    Features:
    - Complex types (List[str], datetime)
    - Automatic datetime handling
    - Tags list support
    """
    global next_article_id

    new_article = {
        "id": next_article_id,
        **article.dict()
    }

    articles_db[next_article_id] = new_article
    next_article_id += 1

    return {
        "success": True,
        "message": "Article created",
        "data": new_article
    }


@app.get("/api/articles/{article_id}", tags=["Articles"])
def get_article(article_id: int):
    """Get article by ID"""
    if article_id not in articles_db:
        raise HTTPException(status_code=404, detail=f"Article {article_id} not found")
    return articles_db[article_id]


@app.get("/api/validation-example", tags=["Examples"])
def validation_example():
    """
    GET /api/validation-example
    Shows validation rules for all models
    """
    return {
        "models": {
            "User": {
                "fields": {
                    "name": "string (2-50 chars)",
                    "email": "valid email format",
                    "age": "integer (18-120)",
                    "is_active": "boolean (default: true)"
                },
                "example": {
                    "name": "Alice Johnson",
                    "email": "alice@example.com",
                    "age": 28,
                    "is_active": True
                }
            },
            "Product": {
                "fields": {
                    "name": "string (1-100 chars, required)",
                    "price": "float (> 0, required)",
                    "stock": "integer (>= 0, optional, default 0)",
                    "description": "string (optional, max 500 chars)",
                    "is_available": "boolean (default: true)"
                },
                "example": {
                    "name": "Laptop Pro",
                    "price": 1299.99,
                    "stock": 10
                }
            },
            "Article": {
                "fields": {
                    "title": "string (5-200 chars)",
                    "content": "string (min 10 chars)",
                    "author": "string (min 2 chars)",
                    "tags": "list of strings (optional)",
                    "published": "boolean (optional)",
                    "created_at": "datetime (optional, auto-generated)"
                }
            }
        }
    }


@app.get("/api/pydantic-info", tags=["Info"])
def pydantic_info():
    """Information about Pydantic features"""
    return {
        "title": "Pydantic Models in FastAPI",
        "features": [
            "Automatic type validation",
            "JSON serialization/deserialization",
            "Field constraints (min_length, max_length, gt, ge, etc)",
            "Custom error messages",
            "Support for complex types (UUID, datetime, email)",
            "Nested models",
            "Optional fields with defaults",
            "Automatic API documentation",
            "Response models for output filtering"
        ],
        "benefits": [
            "Catch errors early",
            "Automatic documentation generation",
            "Type hints for IDE support",
            "Runtime validation"
        ]
    }


if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("FastAPI Demo 2: Pydantic Models")
    print("=" * 70)
    print("\nPydantic Features:")
    print("  Automatic type validation")
    print("  Field constraints (email, ranges, lengths)")
    print("  Complex types (datetime, UUID, email)")
    print("  Partial updates")
    print("  Response models")
    print("\nServer running on http://localhost:8000")
    print("\nTest with curl:")
    print("\n1. Create user (valid):")
    print("   curl -X POST http://localhost:8000/api/users \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"name\":\"Alice\",\"email\":\"alice@example.com\",\"age\":28}'")
    print("\n2. Create user (invalid - wrong email):")
    print("   curl -X POST http://localhost:8000/api/users \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"name\":\"Bob\",\"email\":\"invalid\",\"age\":30}'")
    print("\n3. Create product:")
    print("   curl -X POST http://localhost:8000/api/products \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"name\":\"Laptop\",\"price\":1200.99}'")
    print("\n4. Interactive docs:")
    print("   http://localhost:8000/docs")
    print("\n" + "=" * 70)
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
