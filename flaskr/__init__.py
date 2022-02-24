import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # database path
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite')
    )

    # load config
    if test_config:
        app.config.from_mapping(test_config)
    app.config.from_pyfile('config.py', silent=True)

    # ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)   
    except OSError:
        pass
        
    @app.route('/')
    def hello():
        return "mundo"
    
    return app

