"""Paquete principal de la API REST del blog."""

import connexion

from app.config import Config, DOCS_DIR
from app.extensions import db, ma


def create_app(config_object=Config):
    """Crea y configura una instancia de la aplicación.

    Se usa el patrón application factory para poder crear la aplicación con
    distintas configuraciones (por ejemplo, una base en memoria para tests).
    """
    connex_app = connexion.App(__name__, specification_dir=str(DOCS_DIR))
    app = connex_app.app
    app.config.from_object(config_object)

    # Vincula las extensiones con esta instancia de Flask.
    db.init_app(app)
    ma.init_app(app)

    # Importa los modelos para que SQLAlchemy los registre.
    from app import models  # noqa: F401

    # Registra la vista HTML de inicio.
    from app.routes.home import home_bp

    app.register_blueprint(home_bp)

    # Registra la API definida en docs/swagger.yml.
    connex_app.add_api("swagger.yml")

    return connex_app
