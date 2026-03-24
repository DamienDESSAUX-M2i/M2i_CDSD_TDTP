"""
FastAPI Demo 1: Hello World
Simple FastAPI app with automatic API documentation

FastAPI Features:
    - Automatic OpenAPI documentation at /docs
    - Automatic ReDoc documentation at /redoc
    - Type hints for automatic validation
    - Async/await support

Usage:
    python 01_hello_world.py
    # Server runs on http://localhost:8000

Access Documentation:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
    - OpenAPI JSON: http://localhost:8000/openapi.json

Testing:
    curl http://localhost:8000/
    curl http://localhost:8000/api/hello
    curl "http://localhost:8000/api/hello?name=Alice"
"""

from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI(
    title="FastAPI Hello World Demo",
    description="Simple FastAPI application with automatic documentation",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - returns welcome message"""
    return {
        "message": "Welcome to FastAPI Demo 1!",
        "docs": "Visit http://localhost:8000/docs for interactive API documentation"
    }


@app.get("/api/hello", tags=["Greeting"])
def hello(name: Optional[str] = Query("World", description="Name to greet")):
    """
    Hello endpoint with optional name parameter

    Args:
        name: Name to greet (default: "World")

    Returns:
        dict: JSON response with greeting

    Examples:
        GET /api/hello → {"message": "Hello, World!"}
        GET /api/hello?name=Alice → {"message": "Hello, Alice!"}
    """
    return {
        "message": f"Hello, {name}!",
        "status": "success"
    }


@app.get("/api/info", tags=["Info"])
def info():
    """Returns server information and available endpoints"""
    return {
        "app": "FastAPI Demo 1",
        "version": "1.0.0",
        "framework": "FastAPI",
        "endpoints": [
            {"method": "GET", "path": "/", "description": "Root endpoint"},
            {"method": "GET", "path": "/api/hello", "description": "Hello endpoint"},
            {"method": "GET", "path": "/api/hello?name=YourName", "description": "Hello with name"},
            {"method": "GET", "path": "/api/info", "description": "Server info"},
            {"method": "GET", "path": "/docs", "description": "Interactive API documentation"},
            {"method": "GET", "path": "/redoc", "description": "ReDoc documentation"}
        ],
        "documentation": {
            "swagger_ui": "http://localhost:8000/docs",
            "redoc": "http://localhost:8000/redoc",
            "openapi_json": "http://localhost:8000/openapi.json"
        }
    }


@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "FastAPI Hello World Demo"
    }


if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("FastAPI Demo 1: Hello World")
    print("=" * 70)
    print("\nFastAPI Features:")
    print("  ✓ Automatic API documentation (Swagger UI)")
    print("  ✓ Type hints for automatic validation")
    print("  ✓ Fast performance with async/await support")
    print("  ✓ Built-in data serialization")
    print("\nServer running on http://localhost:8000")
    print("\nAccessible at:")
    print("  Swagger UI:  http://localhost:8000/docs")
    print("  ReDoc:       http://localhost:8000/redoc")
    print("  OpenAPI:     http://localhost:8000/openapi.json")
    print("\nTest with curl:")
    print("  curl http://localhost:8000/api/hello")
    print("  curl 'http://localhost:8000/api/hello?name=Alice'")
    print("\n" + "=" * 70)
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
