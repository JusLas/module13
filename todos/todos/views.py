from flask import Blueprint, jsonify, abort, make_response, request
from .models import Todos


todos_app = Blueprint('todos_app', __name__)


@todos_app.errorhandler(400)
def bad_request(error):
    return make_response(
        jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@todos_app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'error': 'Not found', 'status_code': 404}), 404)


@todos_app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    todos = Todos()
    return jsonify(todos.all())


@todos_app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todos = Todos()
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    
    return jsonify({"todo": todo})


@todos_app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)
    
    todos = Todos()

    todo = {
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
        }
    
    id = todos.create(todo)
    todo['id'] = id
    
    return jsonify({'todo': todo}), 201


@todos_app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todos = Todos()
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    todo = todo[0]
    
    if not request.json:
        abort(400)
    
    data = request.json

    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool) ]):
        abort(400)
    
    todo = {
        'title': data.get('title', todo['title']),
        'description': data.get('description', todo['description']),
        'done': data.get('done', todo['done'])
        }
    todos.update(todo_id, todo)
    todo['id'] = todo_id
    
    return jsonify({'todo': todo})


@todos_app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    todos = Todos()
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    
    return jsonify({'result': result})
