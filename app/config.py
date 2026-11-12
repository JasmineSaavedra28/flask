import pathlib


# Raíz del proyecto: un nivel arriba de la carpeta "app"
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DOCS_DIR = BASE_DIR / "docs"

# Crea la carpeta de la base si todavía no existe.
DATABASE_DIR.mkdir(parents=True, exist_ok=True)


class Config:
    """Configuración común de la aplicación."""

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{(DATABASE_DIR / 'blog.db').as_posix()}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
