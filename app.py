from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    context = {"name": "BASE"}
    return render_template(template_name_or_list="base.html", context=context)


@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
