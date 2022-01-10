from flask import jsonify
from webargs.flaskparser import use_args
from book_library_app import db
from book_library_app.models import Book, BooksSchema
from book_library_app.utils import validate_json_ontent_type, get_schema_args, apply_order, apply_filter, get_pagination
from book_library_app.books import books_bp


@books_bp.route('/books', methods=['GET'])
def get_books():
    query = Book.query
    schema_args = get_schema_args(Book)
    query = apply_order(Book, query)
    query = apply_filter(Book, query)
    items, pagination = get_pagination(query, 'books.get_books')
    books = BooksSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': books,
        'number_of_records': len(books),
        'pagination': pagination
    })