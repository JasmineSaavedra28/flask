import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Raíz del proyecto: un nivel arriba de la carpeta "app"
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DOCS_DIR = BASE_DIR / "docs"

# Crea la carpeta de la base si todavía no existe.
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

connex_app = connexion.App(
    __package__ or __name__,
    specification_dir=str(DOCS_DIR),
)

app = connex_app.app
DATABASE_PATH = (DATABASE_DIR / "blog.db").as_posix()
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
