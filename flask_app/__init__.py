from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
)
from flask_talisman import Talisman
from flask_bcrypt import Bcrypt
import os

# stdlib
from datetime import datetime


db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()


from .users.routes import users
from .landlords.routes import landlords

def page_not_found(e):
    return render_template("404.html"), 404

def create_app():
    app = Flask(__name__)
    #app.config.from_pyfile("config.py", silent=False)
    
    #to run app locally, export the MONGODB_HOST Variable in terminal
    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")
    app.config["SECRET_KEY"] = b'\x020;yr\x91\x11\xbe"\x9d\xc1\x14\x91\xadf\xec'
    csp = {
        'script-src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'
    }

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    Talisman(app, content_security_policy=csp)

    
    app.register_blueprint(users)
    app.register_blueprint(landlords)


    login_manager.login_view = "users.login"
    
    return app
