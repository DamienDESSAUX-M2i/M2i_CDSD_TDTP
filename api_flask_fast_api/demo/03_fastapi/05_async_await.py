"""
FastAPI Demo 5: Async/Await
Demonstrates async operations for high-performance APIs

Async Features:
    - Async route handlers
    - Async dependencies
    - Simulated async I/O (database, HTTP)
    - Concurrent request handling
    - Performance comparison

Usage:
    python 05_async_await.py

Testing:
    # Fast endpoint
    curl http://localhost:8000/api/fast

    # Async endpoint (multiple requests)
    curl http://localhost:8000/api/users/1
    curl http://localhost:8000/api/posts/1

    # Concurrent operations
    curl http://localhost:8000/api/dashboard

    # Compare performance
    curl http://localhost:8000/api/benchmark
"""

import asyncio
import time
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="FastAPI Async/Await Demo",
    description="Demonstrates async operations and high concurrency",
    version="1.0.0"
)


# ============================================================================
# Models
# ============================================================================

class User(BaseModel):
    """User model"""
    id: int
    username: str
    email: str


class Post(BaseModel):
    """Post model"""
    id: int
    user_id: int
    title: str
    content: str


class Comment(BaseModel):
    """Comment model"""
    id: int
    post_id: int
    text: str


class Dashboard(BaseModel):
    """Dashboard model"""
    user: User
    posts: List[Post]
    total_comments: int


# ============================================================================
# Simulated Database Functions
# ============================================================================

async def get_user_from_db(user_id: int) -> Optional[User]:
    """
    Simulate async database call for user
    In real app: await session.query(User).filter(User.id == user_id).first()
    """
    # Simulate network delay (e.g., database query)
    await asyncio.sleep(0.5)

    users = {
        1: User(id=1, username="alice", email="alice@example.com"),
        2: User(id=2, username="bob", email="bob@example.com"),
        3: User(id=3, username="charlie", email="charlie@example.com"),
    }

    return users.get(user_id)


async def get_posts_for_user(user_id: int) -> List[Post]:
    """Simulate async database call for user's posts"""
    await asyncio.sleep(0.3)

    posts_db = {
        1: [
            Post(id=1, user_id=1, title="Python Tips", content="Learn Python..."),
            Post(id=2, user_id=1, title="FastAPI Guide", content="FastAPI tutorial..."),
        ],
        2: [
            Post(id=3, user_id=2, title="Web Dev", content="Web development..."),
        ],
        3: []
    }

    return posts_db.get(user_id, [])


async def get_comments_count(post_id: int) -> int:
    """Simulate async database call for comment count"""
    await asyncio.sleep(0.2)

    # Simulate random counts
    comments_count = {
        1: 5,
        2: 3,
        3: 8
    }

    return comments_count.get(post_id, 0)


async def fetch_external_api(endpoint: str) -> dict:
    """Simulate async HTTP request to external API"""
    await asyncio.sleep(0.4)

    api_responses = {
        "weather": {"temperature": 22, "condition": "sunny"},
        "news": {"headlines": 5, "latest": "Breaking news"},
        "stock": {"price": 150.25, "change": "+2.5%"}
    }

    return api_responses.get(endpoint, {})


# ============================================================================
# Async Dependencies
# ============================================================================

async def get_user_dependency(user_id: int) -> User:
    """Async dependency to get user"""
    user = await get_user_from_db(user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {"message": "FastAPI Async/Await Demo"}


@app.get("/api/fast", tags=["Sync"])
def fast_endpoint():
    """
    Synchronous (blocking) endpoint
    Does not use async - suitable for light operations
    """
    return {
        "message": "Fast response",
        "response_time": "minimal",
        "blocking": True
    }


@app.get("/api/users/{user_id}", response_model=User, tags=["Async"])
async def get_user(user_id: int):
    """
    Async endpoint using async dependency

    Demonstrates:
    - Async route handler
    - Await database call
    - async dependency
    """
    user = await get_user_dependency(user_id)
    return user


@app.get("/api/users/{user_id}/posts", tags=["Async"])
async def get_user_posts(user_id: int):
    """
    Get user's posts asynchronously

    Demonstrates:
    - Multiple async operations
    - Concurrent execution (asyncio.gather)
    """
    start_time = time.time()

    # Verify user exists
    user = await get_user_from_db(user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")

    # Get posts concurrently
    posts = await get_posts_for_user(user_id)

    elapsed = time.time() - start_time

    return {
        "user": user,
        "posts": posts,
        "count": len(posts),
        "execution_time_ms": round(elapsed * 1000, 2)
    }


@app.get("/api/posts/{post_id}", tags=["Async"])
async def get_post_with_comments(post_id: int):
    """
    Get post with comments count

    Demonstrates:
    - Await async database call
    - Return enriched data
    """
    comment_count = await get_comments_count(post_id)

    return {
        "post_id": post_id,
        "comments_count": comment_count,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/dashboard/{user_id}", response_model=Dashboard, tags=["Async"])
async def get_dashboard(user_id: int):
    """
    Get user dashboard with concurrent async operations

    Demonstrates:
    - asyncio.gather() for concurrent operations
    - Performance benefits of async
    """
    start_time = time.time()

    # Get user and posts concurrently
    user, posts = await asyncio.gather(
        get_user_from_db(user_id),
        get_posts_for_user(user_id)
    )

    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")

    # Get comment counts for all posts concurrently
    comment_counts = await asyncio.gather(
        *[get_comments_count(post.id) for post in posts]
    )

    total_comments = sum(comment_counts)
    elapsed = time.time() - start_time

    return {
        "user": user,
        "posts": posts,
        "total_comments": total_comments,
        "execution_time_ms": round(elapsed * 1000, 2)
    }


@app.get("/api/external-data", tags=["Async"])
async def get_external_data():
    """
    Fetch data from multiple external APIs concurrently

    Demonstrates:
    - Multiple concurrent HTTP calls
    - Performance with asyncio.gather()
    """
    start_time = time.time()

    # Fetch from 3 APIs concurrently
    weather, news, stock = await asyncio.gather(
        fetch_external_api("weather"),
        fetch_external_api("news"),
        fetch_external_api("stock")
    )

    elapsed = time.time() - start_time

    return {
        "weather": weather,
        "news": news,
        "stock": stock,
        "execution_time_ms": round(elapsed * 1000, 2),
        "note": "Concurrent execution - much faster than sequential"
    }


@app.get("/api/benchmark", tags=["Performance"])
async def benchmark():
    """
    Performance comparison: sequential vs concurrent

    Shows how async and asyncio.gather() improve performance
    """
    # Sequential execution simulation
    start_seq = time.time()
    result1 = await get_user_from_db(1)
    result2 = await get_posts_for_user(1)
    result3 = await get_comments_count(1)
    seq_time = time.time() - start_seq

    # Concurrent execution using asyncio.gather()
    start_conc = time.time()
    result1, result2, result3 = await asyncio.gather(
        get_user_from_db(1),
        get_posts_for_user(1),
        get_comments_count(1)
    )
    conc_time = time.time() - start_conc

    speedup = seq_time / conc_time

    return {
        "sequential_time_ms": round(seq_time * 1000, 2),
        "concurrent_time_ms": round(conc_time * 1000, 2),
        "speedup_factor": round(speedup, 2),
        "improvement_percent": round((1 - conc_time/seq_time) * 100, 1),
        "note": f"Concurrent is {speedup:.1f}x faster than sequential"
    }


@app.get("/api/async-info", tags=["Info"])
async def async_info():
    """Information about async/await in FastAPI"""
    return {
        "title": "Async/Await in FastAPI",
        "benefits": [
            "Non-blocking I/O",
            "Handle many concurrent requests with fewer threads",
            "Better performance under load",
            "Suitable for I/O-bound operations",
            "Compatible with async libraries"
        ],
        "use_cases": [
            "Database queries",
            "HTTP requests to external APIs",
            "File I/O operations",
            "Message queue operations"
        ],
        "when_to_use": {
            "async": "When endpoint does I/O (database, HTTP calls)",
            "sync": "When endpoint only does CPU-bound operations"
        },
        "concurrency_pattern": {
            "sequential": "await operation1; await operation2; await operation3;",
            "concurrent": "results = await asyncio.gather(op1, op2, op3)"
        }
    }


if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("FastAPI Demo 5: Async/Await")
    print("=" * 70)
    print("\nAsync Benefits:")
    print("   Non-blocking I/O")
    print("   High concurrency with fewer resources")
    print("   Better performance for I/O-bound operations")
    print("   Built-in asyncio.gather() for concurrent operations")
    print("\nServer running on http://localhost:8000")
    print("\nTest with curl:")
    print("\n1. Get user (async):")
    print("   curl http://localhost:8000/api/users/1")
    print("\n2. Get user's posts (concurrent operations):")
    print("   curl http://localhost:8000/api/users/1/posts")
    print("\n3. Dashboard (multiple concurrent calls):")
    print("   curl http://localhost:8000/api/dashboard/1")
    print("\n4. External data (concurrent API calls):")
    print("   curl http://localhost:8000/api/external-data")
    print("\n5. Performance benchmark:")
    print("   curl http://localhost:8000/api/benchmark")
    print("\n6. Multiple concurrent requests (test high concurrency):")
    print("   for i in {1..10}; do curl http://localhost:8000/api/users/1 & done")
    print("\n7. Interactive docs:")
    print("   http://localhost:8000/docs")
    print("\n" + "=" * 70)
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
