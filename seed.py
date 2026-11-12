"""Crea la base blog.db y carga datos de ejemplo.

Uso:
    py seed.py            # crea las tablas y carga datos si la base está vacía
    py seed.py --reset    # borra todo y vuelve a cargar los datos de ejemplo
"""

import argparse

from app import create_app
from app.extensions import db
from app.models import Post, User


def build_sample_users():
    carlos = User(username="carlos_dev", email="carlos@example.com")
    carlos.posts = [
        Post(
            title="Introducción a SQLAlchemy 2.0",
            content=(
                "Primeros pasos con el ORM: engine, sesiones, modelos "
                "declarativos y operaciones CRUD."
            ),
        ),
        Post(
            title="Relaciones avanzadas en el ORM",
            content=(
                "Cómo modelar relaciones uno a muchos con ForeignKey, "
                "back_populates y borrado en cascada."
            ),
        ),
    ]

    ana = User(username="ana_gomez", email="ana@example.com")
    ana.posts = [
        Post(
            title="Primeros pasos con Flask",
            content=(
                "Estructura de una aplicación, blueprints, rutas y "
                "renderizado de plantillas con Jinja."
            ),
        ),
        Post(
            title="Buenas prácticas en APIs REST",
            content=(
                "Recursos, verbos HTTP, códigos de estado y validación "
                "de datos de entrada."
            ),
        ),
    ]

    luis = User(username="luis_rojas", email="luis@example.com")
    luis.posts = [
        Post(
            title="SQLite en proyectos pequeños",
            content=(
                "Ventajas de una base de datos embebida para prácticas, "
                "prototipos y aplicaciones de bajo tráfico."
            ),
        ),
    ]

    return [carlos, ana, luis]


def main():
    parser = argparse.ArgumentParser(description="Inicializa la base del blog.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Borra las tablas existentes antes de cargar los datos.",
    )
    args = parser.parse_args()

    connex_app = create_app()

    with connex_app.app.app_context():
        if args.reset:
            db.drop_all()

        db.create_all()

        if User.query.count() > 0:
            print("La base ya contiene datos. Usá --reset para recrearla.")
            return

        users = build_sample_users()
        db.session.add_all(users)
        db.session.commit()

        print("Base creada correctamente.")
        print(f"Usuarios cargados: {User.query.count()}")
        print(f"Posts cargados: {Post.query.count()}")


if __name__ == "__main__":
    main()
