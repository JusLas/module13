from flask import jsonify, abort, make_response, request
from app.models import Book, Author, BookEvents, book_schema
from app import app, db
from sqlalchemy import desc, exc


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

    return jsonify({'items': book_schema.dump(books, many=True)})


@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    
    return jsonify({'book': book_schema.dump(book)})


@app.route('/api/v1/books/', methods=['POST'])
def create_book():
    data = request.json

    if not data or \
        any([
            not data.get('title', ''),
            not data.get('publication_year', 0)]):
        abort(400)
        
    book = Book(
        title= data['title'],
        publication_year = data['publication_year'],
        read = data.get('read', False)
    )
        
    db.session.add(book)
    db.session.commit()
    
    return jsonify({'book': book_schema.dump(book)}), 201


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
    
    return jsonify({'book': book_schema.dump(book)})


@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
