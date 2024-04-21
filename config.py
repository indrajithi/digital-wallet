class Config:
    """Base configuration with settings common to all environments."""
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///main.db'


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@server/db'


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use an in-memory SQLite database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF forms protection in testing
