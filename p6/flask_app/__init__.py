from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

# local
from .client import RecipeClient  # Changed to use a RecipeClient instead of MovieClient

# update with your API Key
RECIPE_API_KEY = 'd5b9edc50d704fa79875b09d679c8f48'

# do not remove these 2 lines (required for autograder to work)
if os.getenv('RECIPE_API_KEY'):
    RECIPE_API_KEY = os.getenv('RECIPE_API_KEY')

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
recipe_client = RecipeClient(RECIPE_API_KEY)  # Changed to use RecipeClient

from .users.routes import users
from .recipes.routes import recipes  # Changed to 'recipes' blueprint

def custom_404(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(recipes)  # Register the 'recipes' blueprint
    app.register_error_handler(404, custom_404)

    login_manager.login_view = "users.login"

    return app