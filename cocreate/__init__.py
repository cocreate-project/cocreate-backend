from flask import Flask
from cocreate import example, auth

def create_app():
    app = Flask(__name__)
    app.register_blueprint(example.bp)
    app.register_blueprint(auth.bp)
        
    return app