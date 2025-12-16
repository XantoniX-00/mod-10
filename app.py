from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = "secret"

API_URL = os.getenv("API_URL", "http://localhost:5001")

@app.route("/")
def index():
    try:
        r = requests.get(f"{API_URL}/books", timeout=5)
        r.raise_for_status()
        books = r.json()
    except Exception:
        books = []
        flash("Error al conectar con la API", "error")
    return render_template("index.html", books=books)

@app.route("/add", methods=["POST"])
def add():
    data = {
        "title": request.form["title"],
        "author": request.form["author"]
    }
    try:
        r = requests.post(f"{API_URL}/books", json=data, timeout=5)
        r.raise_for_status()
        flash("Libro agregado correctamente", "success")
    except Exception:
        flash("Error al agregar libro", "error")
    return redirect(url_for("index"))

@app.route("/delete/<int:book_id>")
def delete(book_id):
    try:
        r = requests.delete(f"{API_URL}/books/{book_id}", timeout=5)
        r.raise_for_status()
        flash("Libro eliminado", "success")
    except Exception:
        flash("Error al eliminar libro", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)