import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta")

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "flask")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "flask123")
    DB_NAME = os.getenv("DB_NAME", "pi3")