from flask import Flask
from .routes import main_bp
from .monitoring import monitoring_bp
import os

def create_app():
    # PROJECT ROOT (directory of app.py)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        static_folder=os.path.join(project_root, "static")
    )

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(monitoring_bp)

    return app

# 👇 ADD THIS — makes the module export explicit for Linux/GitHub Actions
__all__ = ["create_app"]
