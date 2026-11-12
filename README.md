# Unidad 6 — Backend con Python: relación uno a muchos con Flask

Trabajo práctico que retoma el ejemplo **`02_uno_a_muchos_blog`** de SQLAlchemy y lo
convierte en una aplicación **Flask** con API REST, persistencia en SQLite y
documentación interactiva con Swagger UI.

El tema elegido es un **blog**: un usuario puede escribir muchos posts y cada post
pertenece a un único usuario.

```text
User 1 ---- N Post
```

---

## Tecnologías utilizadas

- **Python 3.14** (probado con 3.14.10)
- **Flask**: framework web del backend.
- **Connexion 3.3**: enlace entre la especificación OpenAPI y las funciones Python.
- **SQLite 3**: base de datos relacional local (`database/blog.db`).
- **Flask-SQLAlchemy / SQLAlchemy 2.x**: ORM y mapeo de la relación.
- **Flask-Marshmallow / Marshmallow**: serialización y deserialización a JSON.
- **Swagger UI**: documentación interactiva de la API.
- **Uvicorn**: servidor ASGI utilizado por Connexion (`app.run()`).

---

## Relación implementada

La relación se toma del ejemplo de la materia:

```python
class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)

    posts: Mapped[list["Post"]] = db.relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan",
        order_by="Post.title",
    )


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    author: Mapped["User"] = db.relationship("User", back_populates="posts")
```

Puntos clave:

- **`ForeignKey("users.id")`** en `Post`: cada post guarda el `id` de su usuario.
- **`User.posts`** es una lista de posts; **`Post.author`** es el usuario dueño.
- **`back_populates`** mantiene sincronizadas ambas direcciones de la relación.
- **`cascade="all, delete-orphan"`** elimina los posts cuando se elimina su usuario.
- **`order_by="Post.title"`** devuelve los posts ordenados alfabéticamente.

---

## Estructura del proyecto

```text
flask/
├── app/
│   ├── __init__.py          # create_app(): application factory
│   ├── config.py            # Clase Config (base de datos, rutas)
│   ├── extensions.py        # Instancias de SQLAlchemy y Marshmallow
│   ├── models/
│   │   ├── __init__.py      # Exporta los modelos
│   │   └── blog.py          # Entidades User y Post
│   ├── schemas/
│   │   ├── __init__.py      # Exporta los esquemas
│   │   ├── post.py          # PostSchema
│   │   └── user.py          # UserSchema con posts anidados
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── helpers.py       # Búsquedas con respuesta 404
│   │   ├── home.py          # Vista HTML de inicio
│   │   ├── posts.py         # Controladores CRUD de posts
│   │   └── users.py         # Controladores CRUD de usuarios
│   └── templates/
│       └── home.html        # Blog que lista usuarios con sus posts
├── database/
│   └── blog.db              # Base SQLite con datos de ejemplo
├── docs/
│   └── swagger.yml          # Especificación OpenAPI 3.0
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Pruebas de integración con base en memoria
├── seed.py                  # Crea/recarga la base con datos de ejemplo
├── run.py                   # Punto de entrada de la aplicación
├── requirements.txt
├── .gitignore
└── README.md
```

### Buenas prácticas aplicadas

- **Application factory (`create_app`)**: la aplicación se construye mediante una
  función, lo que permite crear instancias con configuraciones distintas (por
  ejemplo, una base en memoria para los tests) sin duplicar código.
- **Separación de responsabilidades**:
  - `models/`: entidades y reglas de persistencia.
  - `schemas/`: serialización y deserialización JSON.
  - `routes/`: controladores HTTP.
  - `config.py`: configuración centralizada.
  - `extensions.py`: extensiones inicializadas una sola vez.
- **Blueprints** para la vista HTML, separada de los endpoints de la API.
- **Helpers** para centralizar la búsqueda de recursos y las respuestas `404`.
- **Pruebas automatizadas** con `unittest`, una base SQLite en memoria y
  `StaticPool`, sin tocar la base real.
- **Documentación** de la API con OpenAPI/Swagger y del proyecto en este README.

---

## Instalación y ejecución

Desde la carpeta del proyecto, en PowerShell:

```powershell
# 1. Crear el entorno virtual
py -3.14 -m venv venv

# 2. Activarlo
.\venv\Scripts\Activate.ps1

# Si PowerShell bloquea la activación:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3. Instalar dependencias
python -m pip install -r requirements.txt

# 4. Crear la base y cargar los datos de ejemplo
python seed.py

# 5. Ejecutar la aplicación
python run.py
```

> Si el comando `python` abre la Microsoft Store, usá directamente
> `.\venv\Scripts\python.exe` en los pasos 3, 4 y 5.

Para ejecutar las pruebas automatizadas:

```powershell
python -m unittest discover -s tests -v
```

Luego abrir:

- **Página de inicio:** http://127.0.0.1:8000/
- **Swagger UI:** http://127.0.0.1:8000/api/ui
- **Usuarios:** http://127.0.0.1:8000/api/users
- **Posts:** http://127.0.0.1:8000/api/posts

Para detener el servidor: `Ctrl + C`.

La base `database/blog.db` ya viene creada con datos de ejemplo. Si se borra o se
quiere reiniciar:

```powershell
python seed.py --reset
```

---

## Endpoints de la API

| Acción | Verbo HTTP | Ruta | Descripción |
| :--- | :--- | :--- | :--- |
| Leer usuarios | `GET` | `/api/users` | Lista los usuarios con sus posts anidados. |
| Crear usuario | `POST` | `/api/users` | Crea un usuario. `username` debe ser único. |
| Leer un usuario | `GET` | `/api/users/{user_id}` | Devuelve un usuario con sus posts. |
| Actualizar usuario | `PUT` | `/api/users/{user_id}` | Actualiza `username` y `email`. |
| Eliminar usuario | `DELETE` | `/api/users/{user_id}` | Elimina el usuario y **todos sus posts**. |
| Posts de un usuario | `GET` | `/api/users/{user_id}/posts` | Lista solamente los posts de ese usuario. |
| Leer posts | `GET` | `/api/posts` | Lista todos los posts. |
| Crear post | `POST` | `/api/posts` | Crea un post asociado a un `user_id`. |
| Leer un post | `GET` | `/api/posts/{post_id}` | Devuelve un post. |
| Actualizar post | `PUT` | `/api/posts/{post_id}` | Actualiza el post y permite reasignarlo a otro usuario. |
| Eliminar post | `DELETE` | `/api/posts/{post_id}` | Elimina un post. |

### Ejemplos rápidos (PowerShell)

```powershell
# Listar usuarios con sus posts
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users"

# Crear un usuario
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/users" `
  -ContentType "application/json" `
  -Body '{"username":"maria_lopez","email":"maria@example.com"}'

# Crear un post para ese usuario (usar el id devuelto arriba; por ejemplo 4)
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/posts" `
  -ContentType "application/json" `
  -Body '{"title":"Mi primer post","content":"Hola mundo desde Flask","user_id":4}'

# Ver solamente los posts de ese usuario
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/4/posts"

# Actualizar el post
Invoke-RestMethod -Method Put -Uri "http://127.0.0.1:8000/api/posts/6" `
  -ContentType "application/json" `
  -Body '{"title":"Mi primer post (editado)","content":"Contenido actualizado","user_id":4}'

# Eliminar el usuario: sus posts se borran en cascada
Invoke-RestMethod -Method Delete -Uri "http://127.0.0.1:8000/api/users/4"
```

También se puede probar todo desde **Swagger UI**: http://127.0.0.1:8000/api/ui.

---

## Base de datos

El archivo `database/blog.db` contiene las tablas `users` y `posts` con estos datos
de ejemplo:

| id | username | email | posts |
| :--- | :--- | :--- | :--- |
| 1 | `carlos_dev` | carlos@example.com | 2 |
| 2 | `ana_gomez` | ana@example.com | 2 |
| 3 | `luis_rojas` | luis@example.com | 1 |

Posts cargados:

| Usuario | Posts |
| :--- | :--- |
| `carlos_dev` | Introducción a SQLAlchemy 2.0 · Relaciones avanzadas en el ORM |
| `ana_gomez` | Primeros pasos con Flask · Buenas prácticas en APIs REST |
| `luis_rojas` | SQLite en proyectos pequeños |

Esquema generado por el ORM:

```sql
CREATE TABLE users (
    id INTEGER NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    timestamp DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (username)
);

CREATE TABLE posts (
    id INTEGER NOT NULL,
    title VARCHAR(120) NOT NULL,
    content VARCHAR,
    user_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

> En SQLite la verificación de claves foráneas está desactivada por defecto; el
> borrado en cascada se garantiza igualmente por la configuración del ORM
> (`cascade="all, delete-orphan"`).

---

## Validación realizada

Se probaron los endpoints con el cliente de pruebas ASGI de Connexion
(`create_app().test_client()`) y también con el servidor real levantado con Uvicorn.
Además, `tests/test_api.py` contiene **8 pruebas automatizadas** que usan una base
SQLite en memoria para no modificar `database/blog.db`.

| Prueba | Resultado |
| :--- | :--- |
| `GET /` | `200 OK` — muestra el blog con los 3 usuarios y sus 5 posts. |
| `GET /api/users` | `200 OK` — devuelve los usuarios con los posts anidados. |
| `GET /api/users/1` | `200 OK` — devuelve el usuario y su lista de posts. |
| `GET /api/users/1/posts` | `200 OK` — devuelve solo los posts del usuario. |
| `GET /api/users/999` | `404 Not Found` — usuario inexistente. |
| `POST /api/users` | `201 Created` — crea el usuario. |
| `POST /api/users` con `username` repetido | `406 Not Acceptable` — informa que ya existe. |
| `PUT /api/users/{id}` | `200 OK` — actualiza los datos. |
| `PUT` con `username` de otro usuario | `406 Not Acceptable` — evita duplicados. |
| `POST /api/posts` | `201 Created` — crea el post asociado al usuario. |
| `POST /api/posts` con `user_id` inexistente | `404 Not Found` — el usuario no existe. |
| `PUT /api/posts/{id}` | `200 OK` — actualiza y permite reasignar el post. |
| `DELETE /api/posts/{id}` | `204 No Content` — elimina el post. |
| `DELETE /api/users/{id}` | `204 No Content` — elimina el usuario. |
| `GET` del post tras borrar su usuario | `404 Not Found` — confirma el borrado en cascada. |
| `GET /api/ui` | `200 OK` — carga Swagger UI. |

Resultado de las pruebas automatizadas:

```text
Ran 8 tests in 0.752s

OK
```

Ejemplo de respuesta de `GET /api/users`:

```json
[
  {
    "id": 2,
    "username": "ana_gomez",
    "email": "ana@example.com",
    "timestamp": "2026-11-12T18:25:44.123456",
    "posts": [
      {
        "id": 4,
        "title": "Primeros pasos con Flask",
        "content": "Estructura de una aplicación, blueprints...",
        "user_id": 2,
        "timestamp": "2026-11-12T18:25:44.123456"
      }
    ]
  }
]
```

---

## Notas de implementación

- El proyecto retoma la relación del ejemplo `sqlalchemy/02_uno_a_muchos_blog` y la
  expone mediante Flask, Connexion y Marshmallow.
- La aplicación se crea con `create_app()` (*application factory*). Las extensiones
  `db` y `ma` viven en `app/extensions.py` y se vinculan a cada instancia con
  `init_app()`, lo que permite reutilizar la misma estructura en tests.
- Los modelos `User` y `Post` están juntos en `app/models/blog.py` porque forman
  una misma unidad de dominio y se referencian mutuamente. Los esquemas de
  Marshmallow están separados en `app/schemas/` para no mezclar persistencia con
  serialización.
- La respuesta de un usuario incluye sus posts gracias a
  `posts = fields.Nested(PostSchema, many=True)`. A su vez, `PostSchema` usa
  `include_fk = True` para exponer `user_id`.
- Al crear un post se valida que el `user_id` exista antes de insertar; de lo
  contrario se devuelve `404`.
- En `docs/swagger.yml`, `x-body-name` se ubica dentro de `requestBody`, como
  requiere **Connexion 3.x**.
- El borrado de un usuario elimina sus posts por la cascada del ORM. Además, la
  clave foránea declara `ondelete="CASCADE"`.
- `seed.py` es idempotente: no duplica datos si la base ya tiene usuarios. Con
  `--reset` borra y vuelve a crear todo.
- Las pruebas de `tests/test_api.py` se ejecutan con
  `python -m unittest discover -s tests -v`. Usan `sqlite://` con `StaticPool`
  para compartir una base en memoria entre conexiones.
- `app.run()` de Connexion usa **Uvicorn** como servidor ASGI; por eso `uvicorn`
  forma parte de las dependencias.
- Connexion 3.3 emite un `StarletteDeprecationWarning` sobre `httpx` al iniciar.
  Proviene de la librería y no afecta el funcionamiento.
- Se conserva `datetime.utcnow` para mantener fidelidad con el material; en
  Python 3.12+ puede emitir un aviso de deprecación.

---

## Autora

**Jazmín Saavedra Piñeiro**

Unidad 6 — Backend con Python — Relación Uno a Muchos
