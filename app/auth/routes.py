from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.auth import bp
from app.models import User


@bp.route("/registrati", methods=["GET", "POST"])
def registrati():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        password_conferma = request.form.get("password_conferma", "")

        if not email or not password:
            flash("Email e password sono obbligatorie.", "error")
            return render_template("auth/registrati.html")

        if password != password_conferma:
            flash("Le password non coincidono.", "error")
            return render_template("auth/registrati.html")

        if User.query.filter_by(email=email).first():
            flash("Esiste già un account con questa email.", "error")
            return render_template("auth/registrati.html")

        utente = User(email=email)
        utente.set_password(password)
        db.session.add(utente)
        db.session.commit()

        flash("Registrazione completata. Effettua il login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/registrati.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        utente = User.query.filter_by(email=email).first()

        if utente is None or not utente.check_password(password):
            flash("Email o password non corretti.", "error")
            return render_template("auth/login.html")

        login_user(utente)
        return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.welcome"))