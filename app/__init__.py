from flask import Flask

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    # minimal config
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    # import and register blueprints lazily
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
