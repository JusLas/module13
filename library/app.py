from flask import Flask, jsonify, abort, make_response, request
from models import books


app = Flask(__name__)
app.config['SECRET_KEY'] = 'nininini'


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
    order_by = request.args.get('order_by', 'id')

    return jsonify(books.all(order_by))


@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    
    return jsonify({'book': book})


@app.route('/api/v1/books/', methods=['POST'])
def create_book():
    data = request.json

    if not data or \
        any([
            not data.get('title', ''),
            not data.get('author', ''),
            not data.get('publication_year', 0)]):
        abort(400)
        
    book = {
        'id': books.all()[-1]['id'] + 1,
        'title': data['title'],
        'author': data['author'],
        'publication_year': data['publication_year'],
        'read': data.get('read', False),
        'lent': data.get('lent', False)
        }
        
    books.create(book)
    
    return jsonify({'book': book}), 201


@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    
    if not request.json:
        abort(400)
    
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'publication_year' in data and not isinstance(
            data.get('publication_year'), int),
        'read' in data and not isinstance(data.get('read'), bool),
        'lent' in data and not isinstance(data.get('lent'), bool) ]):
        abort(400)
    
    todo = {
        'id': book_id,
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'publication_year': data.get(
            'publication_year', book['publication_year']),
        'read': data['read'] if 'read' in data else book['read'],
        'lent': data['lent'] if 'lent' in data else book['lent']
        }
    books.update(book_id, todo)
    
    return jsonify({'book': book})


@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
