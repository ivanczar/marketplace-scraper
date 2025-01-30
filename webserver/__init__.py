import os
from flask import Flask
from webserver.routes import main

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), './webserver/templates'),
    )

    app.register_blueprint(main)

    return app
