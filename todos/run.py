from flask import Flask

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # import blueprints
    from todos.views import todos_app

    # register blueprints
    app.register_blueprint(todos_app)

    return app

if __name__ == '__main__':
    app = create_app('config')
    app.run()