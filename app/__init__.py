from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_object='instance.config.Config'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login' 

    # Регистрируем маршруты
    from .routes import user, games
    app.register_blueprint(user.bp)
    app.register_blueprint(games.bp)

    return app
