from flask import Flask
from .auth import auth
from .views import views

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='web'

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")

    return app

