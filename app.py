from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("products.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    return render_template("index.html", products=products)


@app.route("/add", methods=("GET", "POST"))
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
            (name, category, price, stock)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_product.html")


@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit_product(id):
    conn = get_db_connection()

    product = conn.execute(
        "SELECT * FROM products WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]

        conn.execute(
            """
            UPDATE products
            SET name = ?, category = ?, price = ?, stock = ?
            WHERE id = ?
            """,
            (name, category, price, stock, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    conn.close()

    return render_template("edit_product.html", product=product)

@app.route("/delete/<int:id>")
def delete_product(id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM products WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)