from flask import Flask
from flask_cors import CORS


from .utils.modules import import_module_from_path
from .settings import ROOT_PATH, DATABASE_URI, APPS
from .commands import runserver, shell, initdb


def create_app():
    """Creates and configures an instance of the Flask application.

    Returns:
    Flask: An instance of the Flask application.
    """
    # App
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["DATABASE_URI"] = DATABASE_URI

    # CORS
    CORS(app)

    # Default home view
    app.add_url_rule("/", view_func=lambda: {"ping": "pong"}, methods=["GET"])

    # Module views
    for app_name in APPS:
        router_module = import_module_from_path(
            f"{app_name}.router",
            ROOT_PATH / app_name / "router.py",
        )

        app.register_blueprint(
            router_module.router,
            url_prefix=router_module.router.url_prefix or f"/{app_name}",
        )

    # Commands
    app.cli.add_command(runserver)
    app.cli.add_command(shell)
    app.cli.add_command(initdb)

    return app
