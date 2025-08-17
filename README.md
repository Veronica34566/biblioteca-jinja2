# Biblioteca Personal — Flask + Jinja2

Aplicación web de ejemplo que separa la lógica del backend de la presentación usando **Jinja2** (herencia de plantillas, variables, bucles, condicionales) y **Flask**. Permite **agregar**, **actualizar**, **eliminar**, **listar** y **buscar** libros.

## Requisitos
- Python 3.10+
- pip

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar
```bash
# Inicializa la BD con datos de ejemplo (opcional)
flask --app app.py init-db

# Inicia el servidor
flask --app app.py run
# o: python app.py
```

Abre: http://127.0.0.1:5000

## Funcionalidades
- **Listado**: tabla con todos los libros (`/books`).
- **Buscar**: por título, autor, género o año (`/books/search?q=...`).
- **Agregar**: formulario (`/books/new`).
- **Editar**: formulario con datos precargados (`/books/<id>/edit`).
- **Eliminar**: página de confirmación (`/books/<id>/delete`).

## Jinja2 (puntos clave)
- **Herencia**: `templates/base.html` con `{% block %}` y `{% extends %}`.
- **Mensajes flash**: `flash()` en el backend y `get_flashed_messages()` en `templates/_messages.html`.
- **Bucles/condicionales**: tabla del listado (`for`) y estados vacíos (`if`).
- **Separación de responsabilidades**: formularios y tablas generados en plantillas, no en el backend.

## Estructura
```
app.py
requirements.txt
static/css/styles.css
templates/base.html
templates/_messages.html
templates/books/list.html
templates/books/form.html
templates/books/confirm_delete.html
```

## Notas
- Cambia `SECRET_KEY` en `app.py`.
- Para producción, configura `FLASK_ENV=production` y usa un servidor WSGI (gunicorn, etc.).
