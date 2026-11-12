"""Paquete principal de la API REST de la biblioteca."""

from app.config import connex_app
from app.routes.home import home_bp

# Registra la vista HTML de inicio
connex_app.app.register_blueprint(home_bp)

# Registra la API definida en docs/swagger.yml
connex_app.add_api("swagger.yml")

# Alias para ejecutar la aplicación desde run.py
app = connex_app
