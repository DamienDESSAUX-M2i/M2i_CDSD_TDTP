from flask import Flask, jsonify, request

app = Flask(__name__)

books_db = {
    1: {"id": 1, "title": "Titre1", "author": "Author1", "year": 2000},
    2: {"id": 2, "title": "Titre2", "author": "Author1", "year": 2010},
    3: {"id": 3, "title": "Titre3", "author": "Author2", "year": 2010},
}

next_book_id = 4


@app.route("/books", methods=["GET"])
def get_all_books():
    return jsonify(
        {"success": True, "data": list(books_db.values()), "count": len(books_db)}
    ), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    if book_id not in books_db:
        return jsonify({"success": False, "error": f"book {book_id} not found"}), 404

    return jsonify({"success": True, "data": books_db[book_id]}), 200


@app.route("/books", methods=["POST"])
def create_book():
    global next_book_id

    if not request.is_json:
        return jsonify(
            {"success": False, "error": "Content-Type must be application/json"}
        ), 400

    data = request.get_json()
    if not data.get("title") or not data.get("author") or not data.get("year"):
        return jsonify(
            {"success": False, "error": "Missing required fields: title, author, year"}
        ), 400

    for book in books_db.values():
        if book["title"] == data["title"]:
            return jsonify(
                {"success": False, "error": f"Title {data['title']} already exists"}
            ), 409

    new_book = {
        "id": next_book_id,
        "title": data["title"],
        "author": data["author"],
        "year": data["year"],
    }
    books_db[next_book_id] = new_book
    next_book_id += 1

    return jsonify(
        {"success": True, "message": "book created successfully", "data": new_book}
    ), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
