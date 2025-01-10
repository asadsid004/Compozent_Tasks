from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Register Blueprints
    from .routes.home import home

    from .routes.auth import auth

    from .routes.notes import notes

    from .routes.tasks import tasks

    app.register_blueprint(home)
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(notes, url_prefix="/notes")
    app.register_blueprint(tasks, url_prefix="/tasks")

    return app
