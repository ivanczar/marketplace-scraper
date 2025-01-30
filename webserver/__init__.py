import os
from flask import Flask
from webserver.routes import main

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    )

    app.register_blueprint(main)

    return app
