from flask import Flask, render_template, abort, request, redirect, url_for, Response
import sqlite3


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    context = {
        "name": "BASE",
        "project": "Web developer Flask",
    }
    return render_template(template_name_or_list="base.html", **context)


@app.route("/home", methods=["GET"])
def home():
    context = {
        "name": "HOME",
        "my_name": "Jorge",
        "list_languages": ["python", "go", "rust", "js", "ruby"],
    }
    return render_template(template_name_or_list="home.html", **context)


@app.route("/post", methods=["GET"])
def get_all_post():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template(template_name_or_list="post/posts.html", posts=posts)


@app.route("/post/<int:post_id>", methods=["GET"])
def get_one_post(post_id):
    if request.method == "GET":
        conn = get_db_connection()
        post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        conn.close()
        if post is None:
            abort(404)
        return render_template(template_name_or_list="post/post.html", post=post)


@app.route("/post/create", methods=["GET", "POST"])
def create_one_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (title.upper(), content.capitalize()),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("get_all_post"))
    elif request.method == "GET":
        return render_template("post/create.html")


@app.route("/post/edit/<int:post_id>", methods=["GET", "POST"])
def edit_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    print("antes", post["id"], post["title"], post["content"])

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = get_db_connection()
        conn.execute(
            "UPDATE posts SET title = ?, content = ? WHERE id = ?",
            (title, content, post_id),
        )
        conn.commit()
        conn.close()
        conn = get_db_connection()
        post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        conn.close()
        print("despues", post["id"], post["title"], post["content"])
        return redirect(url_for("get_all_post"))

    if request.method == "GET":
        return render_template(template_name_or_list="post/edit.html", post=post)


@app.route("/post/delete/<int:post_id>", methods=["DELETE"])
def delete_one_post(post_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

    return Response(status=200)


if __name__ == "__main__":
    app.run(debug=True)
