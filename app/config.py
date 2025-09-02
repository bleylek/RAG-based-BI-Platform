import os

# ---- OpenAI ve Upload Ayarları ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UPLOAD_FOLDER = "rag_store/uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

# ---- Flask Secret Key ----
SECRET_KEY = os.getenv("SECRET_KEY", "very-secret-key")

# ---- SQLAlchemy Veritabanı Ayarları ----
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ---- Mail Ayarları (Outlook için) ----
MAIL_SERVER = "smtp.office365.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = MAIL_USERNAME
