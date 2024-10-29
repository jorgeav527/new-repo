from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    context = {"name": "BASE"}
    return render_template(template_name_or_list="base.html", context=context)


@app.route("/home", methods=["GET"])
def home():
    context = {"name": "HOME"}
    return render_template(template_name_or_list="home.html", context=context)


if __name__ == "__main__":
    app.run(debug=True)
