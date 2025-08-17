from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "cambia-esta-clave"  # Necesaria para flash()

db = SQLAlchemy(app)

# ----- Modelo -----
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f"<Book {self.title}>"

# ----- Rutas -----
@app.route("/")
def home():
    return redirect(url_for("list_books"))

# Ver listado de libros
@app.route("/books")
def list_books():
    books = Book.query.order_by(Book.title.asc()).all()
    return render_template("books/list.html", books=books)

# Buscar libros (por título/autor/género/año)
@app.route("/books/search")
def search_books():
    q = request.args.get("q", "", type=str).strip()
    results = []
    if q:
        # Si q es número, también intenta por año
        filters = [
            Book.title.ilike(f"%{q}%"),
            Book.author.ilike(f"%{q}%"),
            Book.genre.ilike(f"%{q}%"),
        ]
        if q.isdigit():
            filters.append(Book.year == int(q))
        results = Book.query.filter(or_(*filters)).order_by(Book.title.asc()).all()

    return render_template("books/list.html", books=results, q=q, searching=True)

# Agregar nuevo libro
@app.route("/books/new", methods=["GET", "POST"])
def create_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()
        genre = request.form.get("genre", "").strip()

        if not title or not author:
            flash("Título y Autor son obligatorios.", "error")
            return redirect(url_for("create_book"))

        try:
            y = int(year) if year else None
        except ValueError:
            flash("El año debe ser un número.", "error")
            return redirect(url_for("create_book"))

        new_book = Book(title=title, author=author, year=y, genre=genre or None)
        db.session.add(new_book)
        db.session.commit()
        flash("Libro agregado correctamente.", "success")
        return redirect(url_for("list_books"))

    return render_template("books/form.html", book=None, action="create")

# Actualizar información de un libro
@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()
        genre = request.form.get("genre", "").strip()

        if not title or not author:
            flash("Título y Autor son obligatorios.", "error")
            return redirect(url_for("edit_book", book_id=book.id))

        try:
            y = int(year) if year else None
        except ValueError:
            flash("El año debe ser un número.", "error")
            return redirect(url_for("edit_book", book_id=book.id))

        book.title = title
        book.author = author
        book.year = y
        book.genre = genre or None

        db.session.commit()
        flash("Libro actualizado correctamente.", "success")
        return redirect(url_for("list_books"))

    return render_template("books/form.html", book=book, action="edit")

# Página de confirmación de eliminación
@app.route("/books/<int:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == "POST":
        db.session.delete(book)
        db.session.commit()
        flash("Libro eliminado.", "success")
        return redirect(url_for("list_books"))

    return render_template("books/confirm_delete.html", book=book)

# Inicializar DB con datos demo (opcional)
@app.cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    demo = [
        Book(title="Cien años de soledad", author="Gabriel García Márquez", year=1967, genre="Realismo mágico"),
        Book(title="El Quijote", author="Miguel de Cervantes", year=1605, genre="Novela"),
        Book(title="Rayuela", author="Julio Cortázar", year=1963, genre="Novela"),
    ]
    db.session.add_all(demo)
    db.session.commit()
    print("Base de datos inicializada con datos de ejemplo.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
