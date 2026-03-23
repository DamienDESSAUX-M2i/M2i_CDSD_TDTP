"""
Flask Demo 7: Service Layer and Repository Pattern
Demonstrates separation of concerns with Service and Repository layers

Architecture:
    Controller (Flask routes)
        ↓
    Service (Business logic)
        ↓
    Repository (Data access)
        ↓
    Database (In-memory storage)

Usage:
    python 07_service_layer.py

Testing:
    # Create product
    curl -X POST http://localhost:5000/api/products \
      -H "Content-Type: application/json" \
      -d '{"name":"Laptop","price":1200,"stock":10}'

    # Get product
    curl http://localhost:5000/api/products/1

    # Update product
    curl -X PUT http://localhost:5000/api/products/1 \
      -H "Content-Type: application/json" \
      -d '{"name":"Gaming Laptop","price":1500}'

    # Search products
    curl "http://localhost:5000/api/products/search?min_price=100&max_price=1000"

    # Get high stock products
    curl "http://localhost:5000/api/products/filter?stock_threshold=5"
"""

from datetime import datetime
from typing import Dict, List, Optional

from flask import Flask, jsonify, request

app = Flask(__name__)


# ============================================================================
# Data Models
# ============================================================================


class Product:
    """Product model"""

    def __init__(self, id: int, name: str, price: float, stock: int):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# ============================================================================
# Repository Layer (Data Access)
# ============================================================================


class ProductRepository:
    """
    Repository for Product data access
    Handles all database operations (CRUD)
    """

    def __init__(self):
        self.products: Dict[int, Product] = {}
        self.next_id = 1
        self._initialize_data()

    def _initialize_data(self):
        """Initialize with sample data"""
        self.create(Product(1, "Laptop", 1200, 10))
        self.create(Product(2, "Mouse", 25, 50))
        self.create(Product(3, "Monitor", 300, 15))
        self.create(Product(4, "Keyboard", 75, 30))
        self.next_id = 5

    def create(self, product: Product) -> Product:
        """Create new product"""
        self.products[product.id] = product
        return product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.products.get(product_id)

    def get_all(self) -> List[Product]:
        """Get all products"""
        return list(self.products.values())

    def update(self, product_id: int, **kwargs) -> Optional[Product]:
        """Update product"""
        if product_id not in self.products:
            return None

        product = self.products[product_id]
        for key, value in kwargs.items():
            if hasattr(product, key) and key not in ["id", "created_at"]:
                setattr(product, key, value)
        product.updated_at = datetime.now().isoformat()
        return product

    def delete(self, product_id: int) -> bool:
        """Delete product"""
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False

    def find_by_name(self, name: str) -> List[Product]:
        """Find products by name (case-insensitive)"""
        name_lower = name.lower()
        return [p for p in self.products.values() if name_lower in p.name.lower()]

    def find_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Find products in price range"""
        return [p for p in self.products.values() if min_price <= p.price <= max_price]

    def find_by_stock(self, min_stock: int) -> List[Product]:
        """Find products with minimum stock"""
        return [p for p in self.products.values() if p.stock >= min_stock]

    def get_next_id(self) -> int:
        """Get next available ID"""
        result = self.next_id
        self.next_id += 1
        return result


# ============================================================================
# Service Layer (Business Logic)
# ============================================================================


class ProductService:
    """
    Product service - handles business logic
    Implements CRUD operations and business rules
    """

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_all_products(self) -> List[dict]:
        """Get all products"""
        products = self.repository.get_all()
        return [p.to_dict() for p in products]

    def get_product(self, product_id: int) -> Optional[dict]:
        """Get product by ID"""
        product = self.repository.get_by_id(product_id)
        return product.to_dict() if product else None

    def create_product(self, name: str, price: float, stock: int) -> dict:
        """
        Create new product with validation

        Raises:
            ValueError: If validation fails
        """
        # Validate
        if not name or len(name) < 2:
            raise ValueError("Product name must be at least 2 characters")

        if price <= 0:
            raise ValueError("Price must be greater than 0")

        if stock < 0:
            raise ValueError("Stock cannot be negative")

        # Create product
        product_id = self.repository.get_next_id()
        product = Product(product_id, name, price, stock)
        self.repository.create(product)

        return product.to_dict()

    def update_product(self, product_id: int, **kwargs) -> Optional[dict]:
        """
        Update product with validation

        Raises:
            ValueError: If validation fails
        """
        product = self.repository.get_by_id(product_id)
        if not product:
            return None

        # Validate fields
        if "name" in kwargs:
            if not kwargs["name"] or len(kwargs["name"]) < 2:
                raise ValueError("Product name must be at least 2 characters")

        if "price" in kwargs:
            if kwargs["price"] <= 0:
                raise ValueError("Price must be greater than 0")

        if "stock" in kwargs:
            if kwargs["stock"] < 0:
                raise ValueError("Stock cannot be negative")

        # Update
        updated = self.repository.update(product_id, **kwargs)
        return updated.to_dict() if updated else None

    def delete_product(self, product_id: int) -> bool:
        """Delete product"""
        return self.repository.delete(product_id)

    def search_products(
        self, name: str = None, min_price: float = None, max_price: float = None
    ) -> List[dict]:
        """Search products with filters"""
        results = self.repository.get_all()

        # Filter by name
        if name:
            results = [p for p in results if name.lower() in p.name.lower()]

        # Filter by price range
        if min_price is not None:
            results = [p for p in results if p.price >= min_price]
        if max_price is not None:
            results = [p for p in results if p.price <= max_price]

        return [p.to_dict() for p in results]

    def get_low_stock_products(self, threshold: int = 10) -> List[dict]:
        """Get products with low stock"""
        products = [p for p in self.repository.get_all() if p.stock <= threshold]
        return [p.to_dict() for p in products]

    def get_total_inventory_value(self) -> float:
        """Calculate total value of all inventory"""
        return sum(p.price * p.stock for p in self.repository.get_all())

    def adjust_stock(self, product_id: int, quantity: int) -> Optional[dict]:
        """
        Adjust product stock

        Args:
            product_id: Product ID
            quantity: Quantity to add (negative to subtract)

        Raises:
            ValueError: If resulting stock would be negative
        """
        product = self.repository.get_by_id(product_id)
        if not product:
            return None

        new_stock = product.stock + quantity
        if new_stock < 0:
            raise ValueError("Insufficient stock")

        return self.update_product(product_id, stock=new_stock)


# ============================================================================
# Initialize Layers
# ============================================================================

repository = ProductRepository()
service = ProductService(repository)


# ============================================================================
# Controller Layer (Flask Routes)
# ============================================================================


@app.route("/api/products", methods=["GET"])
def get_all_products():
    """GET /api/products - Get all products"""
    try:
        products = service.get_all_products()
        return jsonify({"success": True, "count": len(products), "data": products}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """GET /api/products/:id - Get specific product"""
    try:
        product = service.get_product(product_id)
        if not product:
            return jsonify(
                {"success": False, "error": f"Product {product_id} not found"}
            ), 404

        return jsonify({"success": True, "data": product}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/products", methods=["POST"])
def create_product():
    """POST /api/products - Create new product"""
    try:
        if not request.is_json:
            return jsonify(
                {"success": False, "error": "Content-Type must be application/json"}
            ), 400

        data = request.get_json()
        required = ["name", "price", "stock"]
        if not all(f in data for f in required):
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing required fields: {', '.join(required)}",
                }
            ), 400

        product = service.create_product(
            name=data["name"], price=float(data["price"]), stock=int(data["stock"])
        )

        return jsonify(
            {"success": True, "message": "Product created", "data": product}
        ), 201

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product_route(product_id):
    """PUT /api/products/:id - Update product"""
    try:
        if not request.is_json:
            return jsonify(
                {"success": False, "error": "Content-Type must be application/json"}
            ), 400

        data = request.get_json()
        kwargs = {}

        if "name" in data:
            kwargs["name"] = data["name"]
        if "price" in data:
            kwargs["price"] = float(data["price"])
        if "stock" in data:
            kwargs["stock"] = int(data["stock"])

        product = service.update_product(product_id, **kwargs)
        if not product:
            return jsonify(
                {"success": False, "error": f"Product {product_id} not found"}
            ), 404

        return jsonify(
            {"success": True, "message": "Product updated", "data": product}
        ), 200

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product_route(product_id):
    """DELETE /api/products/:id - Delete product"""
    try:
        if not service.delete_product(product_id):
            return jsonify(
                {"success": False, "error": f"Product {product_id} not found"}
            ), 404

        return jsonify({"success": True, "message": "Product deleted"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/products/search", methods=["GET"])
def search_products_route():
    """GET /api/products/search?name=...&min_price=...&max_price=..."""
    try:
        name = request.args.get("name")
        min_price = request.args.get("min_price", type=float)
        max_price = request.args.get("max_price", type=float)

        results = service.search_products(name, min_price, max_price)

        return jsonify(
            {
                "success": True,
                "filters": {
                    "name": name,
                    "min_price": min_price,
                    "max_price": max_price,
                },
                "count": len(results),
                "data": results,
            }
        ), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/products/filter", methods=["GET"])
def filter_products():
    """GET /api/products/filter?stock_threshold=10"""
    try:
        threshold = request.args.get("stock_threshold", 10, type=int)
        results = service.get_low_stock_products(threshold)

        return jsonify(
            {
                "success": True,
                "filter": {"stock_threshold": threshold},
                "count": len(results),
                "data": results,
            }
        ), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/products/<int:product_id>/adjust-stock", methods=["POST"])
def adjust_stock(product_id):
    """POST /api/products/:id/adjust-stock - Adjust product stock"""
    try:
        if not request.is_json:
            return jsonify(
                {"success": False, "error": "Content-Type must be application/json"}
            ), 400

        data = request.get_json()
        if "quantity" not in data:
            return jsonify({"success": False, "error": "quantity is required"}), 400

        quantity = int(data["quantity"])
        result = service.adjust_stock(product_id, quantity)

        if not result:
            return jsonify(
                {"success": False, "error": f"Product {product_id} not found"}
            ), 404

        return jsonify(
            {
                "success": True,
                "message": f"Stock adjusted by {quantity}",
                "data": result,
            }
        ), 200

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/inventory/stats", methods=["GET"])
def inventory_stats():
    """GET /api/inventory/stats - Get inventory statistics"""
    try:
        products = service.get_all_products()
        total_value = service.get_total_inventory_value()
        low_stock = service.get_low_stock_products()

        return jsonify(
            {
                "success": True,
                "stats": {
                    "total_products": len(products),
                    "total_inventory_value": round(total_value, 2),
                    "low_stock_count": len(low_stock),
                    "average_stock": round(
                        sum(p["stock"] for p in products) / len(products), 2
                    )
                    if products
                    else 0,
                },
            }
        ), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/architecture", methods=["GET"])
def architecture_info():
    """GET /api/architecture - Shows architecture information"""
    return jsonify(
        {
            "title": "Service Layer Architecture",
            "layers": {
                "controller": "Flask routes - handle HTTP requests",
                "service": "ProductService - business logic",
                "repository": "ProductRepository - data access",
                "model": "Product - data model",
            },
            "flow": "Request → Controller → Service → Repository → Database",
            "benefits": [
                "Separation of concerns",
                "Testability",
                "Reusability",
                "Maintainability",
            ],
        }
    ), 200


if __name__ == "__main__":
    print("=" * 70)
    print("Flask Demo 7: Service Layer and Repository Pattern")
    print("=" * 70)
    print("\nArchitecture: Controller → Service → Repository → Database")
    print("\nService Layer Examples:")
    print("\n1. Get all products:")
    print("   curl http://localhost:5000/api/products")
    print("\n2. Create product:")
    print("   curl -X POST http://localhost:5000/api/products \\")
    print("     -H 'Content-Type: application/json' \\")
    print('     -d \'{"name":"Headphones","price":150,"stock":20}\'')
    print("\n3. Update product:")
    print("   curl -X PUT http://localhost:5000/api/products/1 \\")
    print("     -H 'Content-Type: application/json' \\")
    print('     -d \'{"name":"Gaming Laptop","price":1500}\'')
    print("\n4. Search products:")
    print(
        "   curl 'http://localhost:5000/api/products/search?min_price=100&max_price=500'"
    )
    print("\n5. Adjust stock:")
    print("   curl -X POST http://localhost:5000/api/products/1/adjust-stock \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"quantity\":-5}'")
    print("\n6. Inventory stats:")
    print("   curl http://localhost:5000/api/inventory/stats")
    print("\n" + "=" * 70)
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    app.run(debug=True, port=5000)
