
from flask import Blueprint, jsonify, request
from ..services.book_store import list_books, get_book_by_id, create_book as create_book_service

bp = Blueprint('books', __name__)



@bp.route('/books', methods=['GET'])
def get_books():
    return jsonify(list_books()), 200


@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return jsonify({'error': f'Book with ID {book_id} not found'}), 404
    return jsonify(book), 200


@bp.route('/books', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        result, status = create_book_service(data)
        return jsonify(result), status
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
