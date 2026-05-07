from flask import render_template
from app.main import bp


@bp.route("/")
def home():
    return render_template("main/home.html")


@bp.route("/about")
def about():
    return render_template("main/about.html")