from flask import Flask
from cocreate import example

def create_app():
    app = Flask(__name__)
    app.register_blueprint(example.bp)
        
    return app