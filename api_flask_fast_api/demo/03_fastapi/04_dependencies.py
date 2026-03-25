"""
FastAPI Demo 4: Dependencies
Demonstrates dependency injection for code reuse and separation of concerns

Dependency Features:
    - Reusable business logic
    - Database connections
    - Authentication
    - Common parameter validation
    - Nested dependencies

Usage:
    python 04_dependencies.py

Testing:
    # Pagination dependency
    curl "http://localhost:8000/api/items?skip=0&limit=10"

    # Authentication dependency
    curl -H "X-Token: valid-token" http://localhost:8000/api/protected

    # Without auth token
    curl http://localhost:8000/api/protected

    # Nested dependencies
    curl "http://localhost:8000/api/advanced?skip=0&limit=5&sort=name"
"""

from fastapi import FastAPI, Depends, HTTPException, Query, Header
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(
    title="FastAPI Dependencies Demo",
    description="Demonstrates dependency injection pattern",
    version="1.0.0"
)


# ============================================================================
# Models
# ============================================================================

class Item(BaseModel):
    """Item model"""
    id: int
    name: str
    description: Optional[str] = None
    price: float


class User(BaseModel):
    """User model"""
    id: int
    username: str
    email: str


class PaginationParams(BaseModel):
    """Pagination parameters"""
    skip: int
    limit: int
    total: int
    has_next: bool


# ============================================================================
# Simple Dependencies
# ============================================================================

def get_pagination(
    skip: int = Query(0, ge=0, description="Items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Items to return")
) -> dict:
    """
    Pagination dependency
    Validates and returns pagination parameters
    """
    return {"skip": skip, "limit": limit}


def verify_token(x_token: str = Header(..., description="Authentication token")) -> dict:
    """
    Token verification dependency
    Validates authorization token from headers

    Required header: X-Token
    """
    valid_tokens = ["valid-token", "another-valid-token", "admin-token"]

    if x_token not in valid_tokens:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"token": x_token}


def get_current_user(token: dict = Depends(verify_token)) -> User:
    """
    Get current user dependency
    Uses verify_token dependency to get authenticated user

    Demonstrates nested dependencies
    """
    # Map tokens to users (in real app, would look up in database)
    token_to_user = {
        "valid-token": User(id=1, username="alice", email="alice@example.com"),
        "another-valid-token": User(id=2, username="bob", email="bob@example.com"),
        "admin-token": User(id=3, username="admin", email="admin@example.com")
    }

    user = token_to_user.get(token["token"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


# ============================================================================
# Database-like dependencies
# ============================================================================

items_db = [
    Item(id=1, name="Laptop", description="Gaming laptop", price=1200),
    Item(id=2, name="Mouse", description="Wireless mouse", price=25),
    Item(id=3, name="Keyboard", description="Mechanical keyboard", price=150),
    Item(id=4, name="Monitor", description="4K monitor", price=400),
    Item(id=5, name="Chair", description="Ergonomic chair", price=300),
]


def get_items(pagination: dict = Depends(get_pagination)) -> List[Item]:
    """
    Get items from database with pagination

    Depends on: get_pagination dependency
    """
    skip = pagination["skip"]
    limit = pagination["limit"]
    return items_db[skip:skip + limit]


def get_item_by_id(item_id: int) -> Item:
    """Get specific item by ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


# ============================================================================
# Advanced Dependencies
# ============================================================================

class CommonQueryParams:
    """
    Reusable query parameters
    Can be used as a class-based dependency
    """
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        sort: str = Query("id", regex="^[a-z_]+$")
    ):
        self.skip = skip
        self.limit = limit
        self.sort = sort


def sort_items(items: List[Item], sort_by: str) -> List[Item]:
    """Helper function to sort items"""
    sort_key_map = {
        "id": lambda x: x.id,
        "name": lambda x: x.name,
        "price": lambda x: x.price
    }

    key_func = sort_key_map.get(sort_by, lambda x: x.id)
    return sorted(items, key=key_func)


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
def root():
    """Root endpoint"""
    return {"message": "FastAPI Dependencies Demo"}


@app.get("/api/items", response_model=dict, tags=["Items"])
def list_items(pagination: dict = Depends(get_pagination)):
    """
    Get items with pagination

    Uses: get_pagination dependency

    Query Parameters:
        skip: number of items to skip
        limit: maximum items to return (1-100)
    """
    items = items_db[pagination["skip"]:pagination["skip"] + pagination["limit"]]

    return {
        "data": items,
        "pagination": {
            "skip": pagination["skip"],
            "limit": pagination["limit"],
            "total": len(items_db),
            "returned": len(items)
        }
    }


@app.get("/api/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(item: Item = Depends(get_item_by_id)):
    """
    Get specific item by ID

    Uses: get_item_by_id dependency

    Returns 404 if item not found
    """
    return item


@app.get("/api/protected", tags=["Auth"])
def protected_endpoint(user: User = Depends(get_current_user)):
    """
    Protected endpoint requiring authentication

    Uses: get_current_user dependency (which uses verify_token)

    Required header: X-Token
    """
    return {
        "message": f"Hello, {user.username}!",
        "user": user,
        "message_detail": "This is a protected endpoint"
    }


@app.get("/api/admin", tags=["Auth"])
def admin_endpoint(user: User = Depends(get_current_user)):
    """
    Admin endpoint - only accessible with valid token

    Checks if user is admin before allowing access
    """
    if user.username != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {
        "message": "Welcome, admin!",
        "user": user,
        "admin_data": {
            "total_users": 3,
            "total_items": len(items_db),
            "system_status": "operational"
        }
    }


@app.get("/api/advanced", tags=["Items"])
def advanced_listing(
    commons: CommonQueryParams = Depends(),
    user: User = Depends(get_current_user)
):
    """
    Advanced listing with sorting and authentication

    Uses:
    - CommonQueryParams: reusable query parameters
    - get_current_user: authentication dependency

    Demonstrates stacking multiple dependencies
    """
    items = items_db[commons.skip:commons.skip + commons.limit]
    sorted_items = sort_items(items, commons.sort)

    return {
        "message": f"Listing items for user {user.username}",
        "pagination": {
            "skip": commons.skip,
            "limit": commons.limit,
            "sort": commons.sort
        },
        "data": sorted_items
    }


@app.get("/api/my-items", tags=["Items"])
def my_items(
    user: User = Depends(get_current_user),
    pagination: dict = Depends(get_pagination)
):
    """
    Get user's items

    Uses multiple dependencies:
    - get_current_user: authentication
    - get_pagination: pagination parameters

    Demonstrates how FastAPI handles multiple dependencies
    """
    return {
        "message": f"Items for user {user.username}",
        "items": items_db[pagination["skip"]:pagination["skip"] + pagination["limit"]],
        "pagination": pagination
    }


@app.get("/api/dependencies-info", tags=["Info"])
def dependencies_info():
    """Information about dependency injection"""
    return {
        "title": "FastAPI Dependency Injection",
        "benefits": [
            "Code reuse",
            "Separation of concerns",
            "Easy testing",
            "Automatic documentation",
            "Authentication/Authorization",
            "Database connections",
            "Common validations"
        ],
        "examples": {
            "simple_dependency": "Function that validates parameters",
            "database_dependency": "Function that fetches data",
            "authentication": "Function that verifies token",
            "nested_dependency": "Dependency that uses other dependencies",
            "class_dependency": "Class-based dependency for complex parameters"
        }
    }


if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("FastAPI Demo 4: Dependencies")
    print("=" * 70)
    print("\nDependency Types:")
    print("  Simple dependencies (functions)")
    print("  Nested dependencies")
    print("  Class-based dependencies")
    print("  Authentication/Authorization")
    print("  Database connections")
    print("  Common parameters")
    print("\nServer running on http://localhost:8000")
    print("\nTest with curl:")
    print("\n1. Get items (with pagination):")
    print("   curl 'http://localhost:8000/api/items?skip=0&limit=2'")
    print("\n2. Get specific item:")
    print("   curl http://localhost:8000/api/items/1")
    print("\n3. Protected endpoint (requires token):")
    print("   curl -H 'X-Token: valid-token' http://localhost:8000/api/protected")
    print("\n4. Admin endpoint:")
    print("   curl -H 'X-Token: admin-token' http://localhost:8000/api/admin")
    print("\n5. Without token (401 error):")
    print("   curl http://localhost:8000/api/protected")
    print("\n6. Advanced listing (multiple dependencies):")
    print("   curl -H 'X-Token: valid-token' \\")
    print("     'http://localhost:8000/api/advanced?skip=0&limit=3&sort=name'")
    print("\n7. Interactive docs:")
    print("   http://localhost:8000/docs")
    print("\n" + "=" * 70)
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
