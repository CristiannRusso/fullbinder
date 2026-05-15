from datetime import datetime, timezone
from app import db


class Binder(db.Model):
    __tablename__ = "binders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    tag_name = db.Column(db.String(255), db.ForeignKey("tags.name"), nullable=False)
    pinned = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    documents = db.relationship(
        "Document",
        backref="binder",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    tag = db.relationship(
        "Tag", 
        backref=db.backref("binders", lazy="dynamic")
    )

    def __repr__(self):
        return f"<Binder {self.name}>"


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False, unique=True)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    binder_id = db.Column(db.Integer, db.ForeignKey("binders.id"), nullable=False)

    def __repr__(self):
        return f"<Document {self.original_name}>"

class Tag(db.Model):
    __tablename__ = "tags"
    name = db.Column(db.String(255), primary_key=True)
    color = db.Column(db.String(7), nullable=False, default="#3B5BDB")

    def __repr__(self):
        return f"<Tag {self.name}>"