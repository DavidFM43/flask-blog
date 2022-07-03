import os
from flask import Flask
from . import db
from . import auth
from . import blog


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # database path
        DATABASE=os.path.join(app.instance_path, "flask.sqlite"),
    )

    # load test config if there is one
    if test_config:
        app.config.from_mapping(test_config)
    app.config.from_pyfile("config.py", silent=True)

    # ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hola mundo"

    # register the database methods
    db.init_app(app)

    # register auth blueprint
    app.register_blueprint(auth.bp)

    # register blog blueprint
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app
