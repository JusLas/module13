from flask import Flask

def create_app():
    app = Flask(__name__)
    
    import config
    app.config.from_object(config)

    # import blueprints
    from todos.views import todos_app

    # register blueprints
    app.register_blueprint(todos_app)

    from db.utils import init_app
    init_app(app)


    return app

if __name__ == '__main__':
    app = create_app()
    app.run()