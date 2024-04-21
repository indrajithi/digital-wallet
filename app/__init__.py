from flask import Flask
from .extensions import db, migrate


def create_app(config_name=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wallet.db'
        app.config['DEBUG'] = True
    
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_timeout': 30
    }
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main as main_routes
    app.register_blueprint(main_routes)

    return app
