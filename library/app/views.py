from datetime import datetime

from flask import abort, jsonify, make_response, request
from sqlalchemy import desc, exc

from app import app, db
from app.models import Author, Book, BookEvents, book_with_authors_schema


@app.errorhandler(400)
def bad_request(error):
    return make_response(
        jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.route('/api/v1/books/', methods=['GET'])
def books_list_api_v1():
    books = Book.query.all()

    order_by = request.args.get('order_by', 'id')
    if order_by and isinstance(order_by, str):
        revese = False
        if order_by[0] == '-':
            revese = True
            order_by = order_by[1:]
        try:
            if revese:
                books = Book.query.order_by(desc(order_by)).all()
            else:
                books = Book.query.order_by(order_by).all()
        except exc.CompileError:
            pass

    return jsonify({'items': book_with_authors_schema.dump(books, many=True)})


@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    
    return jsonify({'book': book_with_authors_schema.dump(book)})


@app.route('/api/v1/books/', methods=['POST'])
def create_book():
    data = request.json

    authors = data.get('authors', [])
    if not data or \
        any([
            not data.get('title', ''),
            not data.get('publication_year', 0),
            not authors]):
        abort(400)
    
    for author in authors:
        if not 'first_name' in author or \
            not 'last_name' in author:
            abort(400)
        
    book = Book(
        title= data['title'],
        publication_year = data['publication_year'],
        read = data.get('read', False)
    )

    authors_temp = []

    for author in authors:
        existing = Author.query.filter_by(
            first_name=author['first_name'], last_name=author['last_name']
            ).first()
        if existing:
            authors_temp.append(existing)
        else:
            created = Author(
                first_name = author['first_name'],
                last_name = author['last_name']
            )
            db.session.add(created)
            db.session.commit()
            authors_temp.append(created)
    
    book.authors = authors_temp
        
    db.session.add(book)
    db.session.commit()
    
    return jsonify({'book': book_with_authors_schema.dump(book)}), 201


@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    
    if not request.json:
        abort(400)
    
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'publication_year' in data and not isinstance(
            data.get('publication_year'), int),
        'read' in data and not isinstance(data.get('read'), bool)]):
        abort(400)
    
    book.title = data.get('title', book.title)
    book.publication_year = data.get(
            'publication_year', book.publication_year)
    book.read = data['read'] if 'read' in data else book.read

    db.session.add(book)
    db.session.commit()
    
    return jsonify({'book': book_with_authors_schema.dump(book)})


@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'result': True})


@app.route('/api/v1/books/lent', methods=['POST'])
def lent_book():
    data = request.json
    if not data or not data.get('book_id', ''):
        abort(400)

    book = Book.query.get(data['book_id'])

    if not book:
        abort(404)

    for e in book.events:
        if e.lent and not e.returned:
            return jsonify({'result': False})
    
    event = BookEvents(lent=datetime.utcnow(), book=book)
    db.session.add(event)
    db.session.commit()
    
    return jsonify({'result': True})


@app.route('/api/v1/books/return', methods=['POST'])
def return_book():
    data = request.json
    if not data or not data.get('book_id', ''):
        abort(400)

    book = Book.query.get(data['book_id'])

    if not book:
        abort(404)

    for e in book.events:
        if e.lent and not e.returned:
            e.returned = datetime.utcnow()
            db.session.add(e)
            db.session.commit()
            return jsonify({'result': True})
    
    
    return jsonify({'result': False})
