from flask import jsonify, abort
from webargs.flaskparser import use_args
from book_library_app import db
from book_library_app.models import Book, BooksSchema, book_schema, Author
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

@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int):
    book = Book.query.get_or_404(book_id, description= f'Book with id {book_id} not found')
    return jsonify({
        'success': True,
        'data': book_schema.dump(book)
    })

@books_bp.route('/books/<int:book_id>', methods=['PUT'])
@validate_json_ontent_type
@use_args(book_schema, error_status_code=400)
def update_book(args: dict, book_id: int):
    book = Book.query.get_or_404(book_id, description= f'Book with id {book_id} not found')
    if Book.query.filter(Book.isbn == args['isbn']).first():
        abort(409, description=f'Book with ISBN {args["isbn"]} already exists')

    book.title = args['title']
    book.isbn = args['isbn']
    book.number_of_pages = args['number_of_pages']
    description = args.get('description')
    if description is not None:
        book.description = args['description']
    author_id = args.get('author_id')

    if author_id is not None:
        Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')
        book.author_id = args['author_id']

    db.session.commit()

    return jsonify({
        'success': True,
        'data': book_schema.dump(book)
    })