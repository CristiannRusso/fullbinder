import os

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-me"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        f"sqlite:///{os.path.join(basedir, 'instance', 'fullbinder.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")