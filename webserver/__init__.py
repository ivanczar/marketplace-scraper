from flask import Flask
import os

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), './webserver/templates'),
    )
    
    from webserver.routes import main
    app.register_blueprint(main)
    
    return app
