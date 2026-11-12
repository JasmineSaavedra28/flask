import unittest

from sqlalchemy.pool import StaticPool

from app import create_app
from app.config import Config
from app.extensions import db
from app.models import Post, User


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }


class BlogApiTestCase(unittest.TestCase):
    """Pruebas de integración de la API y de la relación uno a muchos."""

    @classmethod
    def setUpClass(cls):
        cls.connex_app = create_app(TestConfig)
        cls.client = cls.connex_app.test_client()

    def setUp(self):
        with self.connex_app.app.app_context():
            db.drop_all()
            db.create_all()

            user = User(username="carlos_dev", email="carlos@example.com")
            user.posts = [
                Post(title="Introducción a SQLAlchemy", content="Contenido"),
                Post(title="Flask y APIs", content="Contenido"),
            ]
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        with self.connex_app.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_muestra_usuarios_y_posts(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Blog de la comunidad", response.text)
        self.assertIn("carlos_dev", response.text)

    def test_listar_usuarios_con_posts_anidados(self):
        response = self.client.get("/api/users")

        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertEqual(len(users), 1)
        self.assertEqual(len(users[0]["posts"]), 2)

    def test_crear_usuario(self):
        response = self.client.post(
            "/api/users",
            json={"username": "ana_gomez", "email": "ana@example.com"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "ana_gomez")

    def test_no_permite_username_duplicado(self):
        response = self.client.post(
            "/api/users",
            json={"username": "carlos_dev", "email": "otro@example.com"},
        )

        self.assertEqual(response.status_code, 406)

    def test_crear_post_asociado_a_usuario(self):
        response = self.client.post(
            "/api/posts",
            json={
                "title": "Nuevo post",
                "content": "Contenido",
                "user_id": self.user_id,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["user_id"], self.user_id)

    def test_no_permite_post_de_usuario_inexistente(self):
        response = self.client.post(
            "/api/posts",
            json={"title": "Huérfano", "user_id": 999},
        )

        self.assertEqual(response.status_code, 404)

    def test_eliminar_usuario_elimina_sus_posts(self):
        posts = self.client.get(f"/api/users/{self.user_id}/posts").json()
        post_id = posts[0]["id"]

        response = self.client.delete(f"/api/users/{self.user_id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/api/posts/{post_id}")
        self.assertEqual(response.status_code, 404)

    def test_buscar_usuario_inexistente(self):
        response = self.client.get("/api/users/999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
