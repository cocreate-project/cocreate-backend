from flask import Flask
from cocreate import auth, generate, settings

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth.bp)
    app.register_blueprint(generate.bp)
    app.register_blueprint(settings.bp)

    return app