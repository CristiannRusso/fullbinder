from flask import render_template, redirect, url_for, request, flash
from app import db
from app.main import bp
from app.models import Binder, Document


COLORI_BINDER = [
    {"hex": "#C44918", "nome": "Arancio"},
    {"hex": "#2A4A6B", "nome": "Blu"},
    {"hex": "#C99529", "nome": "Senape"},
    {"hex": "#6B3D5E", "nome": "Prugna"},
    {"hex": "#6E8265", "nome": "Salvia"},
    {"hex": "#4A4F58", "nome": "Grafite"},
]


def _sidebar_data():
    """Dati comuni a tutte le viste della dashboard (sidebar)."""
    binders_pinned = Binder.query.filter_by(pinned=True).order_by(Binder.created_at.desc()).all()
    binders_normali = Binder.query.filter_by(pinned=False).order_by(Binder.created_at.desc()).all()
    total_binders = Binder.query.count()
    total_documents = Document.query.count()
    return {
        "binders_pinned": binders_pinned,
        "binders_normali": binders_normali,
        "total_binders": total_binders,
        "total_documents": total_documents,
    }


@bp.route("/")
def dashboard():
    return render_template(
        "main/dashboard.html",
        view_mode="all_binders",
        open_binder=None,
        **_sidebar_data(),
    )


@bp.route("/documents")
def all_documents():
    documenti = Document.query.order_by(Document.uploaded_at.desc()).all()
    return render_template(
        "main/dashboard.html",
        view_mode="all_documents",
        open_binder=None,
        documenti=documenti,
        **_sidebar_data(),
    )


@bp.route("/binders/<int:binder_id>")
def binder_view(binder_id):
    binder = Binder.query.get_or_404(binder_id)
    documenti = binder.documents.order_by(Document.uploaded_at.desc()).all()
    return render_template(
        "main/dashboard.html",
        view_mode="binder",
        open_binder=binder,
        documenti=documenti,
        **_sidebar_data(),
    )


@bp.route("/binders/new", methods=["GET", "POST"])
def new_binder():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        descrizione = request.form.get("descrizione", "").strip()
        color = request.form.get("color", "#C44918")
        tag = request.form.get("tag", "").strip() or "Generale"

        if not nome:
            flash("Il nome del raccoglitore è obbligatorio.", "error")
            return render_template("main/new_binder.html", colori=COLORI_BINDER)

        valori_color_validi = [c["hex"] for c in COLORI_BINDER]
        if color not in valori_color_validi:
            color = "#C44918"

        binder = Binder(name=nome, description=descrizione, color=color, tag=tag)
        db.session.add(binder)
        db.session.commit()

        return redirect(url_for("main.binder_view", binder_id=binder.id))

    return render_template("main/new_binder.html", colori=COLORI_BINDER)