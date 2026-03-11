import os
from flask import Flask
from .config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Registrar blueprints
    from .routes.main_routes import main
    from .routes.auth_routes import auth
    from .routes.evento_routes import evento

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(evento)

    return app