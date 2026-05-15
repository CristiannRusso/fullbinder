import os
import uuid
from flask import render_template, redirect, url_for, request, flash, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app import db
from app.main import bp
from app.models import Binder, Document, Tag


TAG_COLORS = [
    {"hex": "#3B5BDB", "nome": "Indigo"},
    {"hex": "#1C7ED6", "nome": "Sky"},
    {"hex": "#0CA678", "nome": "Teal"},
    {"hex": "#5C940D", "nome": "Moss"},
    {"hex": "#F08C00", "nome": "Amber"},
    {"hex": "#E8590C", "nome": "Pumpkin"},
    {"hex": "#C92A2A", "nome": "Brick"},
    {"hex": "#D6336C", "nome": "Rose"},
    {"hex": "#7048E8", "nome": "Violet"},
    {"hex": "#495057", "nome": "Slate"},
]


def _sidebar_data():
    """Dati comuni a tutte le viste della dashboard (sidebar)."""
    pinned_binders = Binder.query.filter_by(pinned=True).all()
    normal_binders = Binder.query.filter_by(pinned=False).all()
    normal_tags = Tag.query.all()
    total_binders = Binder.query.count()
    total_documents = Document.query.count()
    total_tags = Tag.query.count()
    return {
        "pinned_binders": pinned_binders,
        "normal_binders": normal_binders,
        "normal_tags": normal_tags,
        "total_binders": total_binders,
        "total_documents": total_documents,
        "total_tags": total_tags,
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


@bp.route("/binders/<string:name>")
def tag_view(name):
    tag = Tag.query.get_or_404(name)
    return render_template(
        "main/dashboard.html",
        view_mode="tag",
        open_tag=tag,
        **_sidebar_data(),
    )


@bp.route("/binders/new", methods=["POST"])
def new_binder():
    nome = request.form.get("nome", "").strip()
    descrizione = request.form.get("descrizione", "").strip()
    color = request.form.get("color", "#C44918")
    tag = request.form.get("tag", "").strip() or "Generale"

    if not nome:
        flash("Name is required", "error")
        return redirect(url_for("main.dashboard"))

    tag_obj = Tag.query.filter_by(name=tag).first()
    if not tag_obj:
        flash(f"Il tag '{tag}' non esiste. Crealo prima.", "error")
        return redirect(url_for("main.dashboard"))

    binder = Binder(name=nome, description=descrizione, tag_name=tag)
    db.session.add(binder)
    db.session.commit()

    return redirect(url_for("main.binder_view", binder_id=binder.id))

@bp.route("/tags/new", methods=["POST"])
def new_tag():
    name_tag = request.form.get("nome-tag").strip()
    color = request.form.get("color", "#3B5BDB")

    if not name_tag:
        flash("Name is required", "error")
        return redirect(url_for("main.dashboard"))
    
    tag_check = Tag.query.filter_by(name=name_tag).first()

    if tag_check:
        flash("Tag already exists", "error")
        return redirect(url_for("main.dashboard"))
    
    valid_color = [c["hex"] for c in TAG_COLORS]
    if color not in valid_color:
        color = "#3B5BDB"

    tag = Tag(name=name_tag, color=color)
    db.session.add(tag)
    db.session.commit()

    return redirect(url_for("main.dashboard"))

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

@bp.route("/binders/<int:binder_id>/upload", methods=["POST"])
def binder_upload(binder_id):
    binder = Binder.query.get_or_404(binder_id)

    if "files" not in request.files:
        flash("Nessun file selezionato.", "error")
        return redirect(url_for("main.binder_view", binder_id=binder.id))

    files = request.files.getlist("files")
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    salvati = 0
    for f in files:
        if not f or not f.filename:
            continue

        nome_originale = f.filename
        nome_sicuro = secure_filename(nome_originale)
        if not nome_sicuro:
            continue

        estensione = ""
        if "." in nome_sicuro:
            estensione = "." + nome_sicuro.rsplit(".", 1)[1].lower()

        nome_archiviato = uuid.uuid4().hex + estensione
        percorso = os.path.join(upload_folder, nome_archiviato)
        f.save(percorso)

        documento = Document(
            original_name=nome_originale,
            stored_name=nome_archiviato,
            binder_id=binder.id,
        )
        db.session.add(documento)
        salvati += 1

    if salvati > 0:
        db.session.commit()

    return redirect(url_for("main.binder_view", binder_id=binder.id))


@bp.route("/documents/<int:doc_id>/download")
def document_download(doc_id):
    documento = Document.query.get_or_404(doc_id)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(
        upload_folder,
        documento.stored_name,
        as_attachment=True,
        download_name=documento.original_name,
    )

@bp.route("/binders/<int:binder_id>/edit", methods=["POST"])
def binder_edit(binder_id):
    binder = Binder.query.get_or_404(binder_id)

    nome = request.form.get("nome", "").strip()
    descrizione = request.form.get("descrizione", "").strip()
    tag = request.form.get("tag", "").strip()

    if not nome:
        flash("Il nome del raccoglitore è obbligatorio.", "error")
        return redirect(url_for("main.binder_view", binder_id=binder.id))

    tag_obj = Tag.query.filter_by(name=tag).first()
    if not tag_obj:
        flash(f"Il tag '{tag}' non esiste.", "error")
        return redirect(url_for("main.binder_view", binder_id=binder.id))

    binder.name = nome
    binder.description = descrizione
    binder.tag_name = tag
    db.session.commit()

    return redirect(url_for("main.binder_view", binder_id=binder.id))


@bp.route("/binders/<int:binder_id>/delete", methods=["POST"])
def binder_delete(binder_id):
    binder = Binder.query.get_or_404(binder_id)

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    for documento in binder.documents.all():
        percorso = os.path.join(upload_folder, documento.stored_name)
        if os.path.exists(percorso):
            try:
                os.remove(percorso)
            except OSError:
                pass

    db.session.delete(binder)
    db.session.commit()

    return redirect(url_for("main.dashboard"))