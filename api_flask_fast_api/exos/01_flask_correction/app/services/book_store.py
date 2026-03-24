from datetime import datetime


books_db = {
    1: {'id': 1, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'year': 1960},
    2: {'id': 2, 'title': '1984', 'author': 'George Orwell', 'year': 1949}
}
next_book_id = 3


def list_books():
    return list(books_db.values())


def get_book_by_id(book_id: int):
    return books_db.get(book_id)


def create_book(data: dict):
    global next_book_id

    if not data.get('title') or not data.get('author'):
        return {
            'error': 'Missing required fields',
            'required': ['title', 'author'],
            'optional': ['year']
        }, 422

    title = data['title'].strip()
    if len(title) < 1:
        return {'error': 'Title cannot be empty'}, 422

    author = data['author'].strip()
    if len(author) < 1:
        return {'error': 'Author cannot be empty'}, 422

    year = None
    if 'year' in data:
        try:
            year = int(data['year'])
            if year < 1000 or year > datetime.now().year + 10:
                return {
                    'error': 'Year must be valid',
                    'range': [1000, datetime.now().year + 10]
                }, 422
        except (ValueError, TypeError):
            return {'error': 'Year must be an integer'}, 422

    book = {
        'id': next_book_id,
        'title': title,
        'author': author,
        'year': year
    }
    books_db[next_book_id] = book
    next_book_id += 1
    return book, 201
