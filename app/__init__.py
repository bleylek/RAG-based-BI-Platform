# app/__init__.py
from flask import Flask
from app.extensions import mail
from app.auth.routes import auth_bp
from app.auth.models import db



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    
    # Uygulamaya veritabanını tanıtma
    db.init_app(app)
    
    # Uygulama kontekstinde veritabanını oluşturma
    with app.app_context():
        try:
            db.create_all()
            print("Veritabanı başarıyla oluşturuldu.")
        except Exception as e:
            print(f"Veritabanı oluşturma hatası: {e}")
            # Veritabanı dosyası erişim izinlerini kontrol et
            import os
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            print(f"Veritabanı yolu: {db_path}")
            if os.path.exists(db_path):
                print(f"Veritabanı dosyası mevcut, izinler: {os.stat(db_path)}")
            else:
                print(f"Veritabanı dosyası bulunamadı. Dizin içeriği: {os.listdir(os.path.dirname(db_path) if os.path.dirname(db_path) else '.')}")
        
    mail.init_app(app)
    
    from .routes.main_routes import main_bp
    from .routes.rag_routes import rag_bp
    from .routes.offer_routes import offer_bp
    from .routes.contract_routes import contract_bp
    from .routes.message_routes import message_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(rag_bp)
    app.register_blueprint(offer_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(auth_bp)

    return app