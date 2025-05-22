from flask import Flask
from cocreate import auth, generate, settings, generations, user

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth.bp)
    app.register_blueprint(generate.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(generations.bp)
    app.register_blueprint(user.bp)

    return app