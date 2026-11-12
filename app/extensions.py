from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Extensiones compartidas. Se inicializan en create_app() mediante init_app().
db = SQLAlchemy()
ma = Marshmallow()
