# Kullanıcı modelini tanımlıyoruz bu dosyada

# app/auth/models.py
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy: Flask ile entegre çalışan ORM (Object-Relational Mapper) kütüphanesidir. Python sınıflarını veri tabanı tablolarına dönüştürür.
from datetime import datetime # datetime: Kullanıcı oluşturulma tarihini kaydetmek için kullanılır.
from werkzeug.security import generate_password_hash, check_password_hash # werkzeug.security: Parola güvenliği için hashleme ve doğrulama fonksiyonları sağlar.

db = SQLAlchemy() # Flask uygulamasında kullanılacak SQLAlchemy örneğini oluşturur.

class User(db.Model): # User sınıfı, veritabanında bir "users" tablosuna karşılık gelir.
    id = db.Column(db.Integer, primary_key=True) # Her kullanıcıya özel bir birincil anahtar (primary key) olan tamsayı ID.
    email = db.Column(db.String(120), unique=True, nullable=False) # Maksimum 120 karakter uzunluğunda, benzersiz ve boş geçilemez e-posta alanı.
    password_hash = db.Column(db.String(128), nullable=False) # Şifrenin kendisi değil, hashlenmiş versiyonu burada tutulur. Güvenlik amacıyla düz şifre saklanmaz.
    is_verified = db.Column(db.Boolean, default=False) # Kullanıcının e-posta doğrulamasını yapıp yapmadığını tutan boolean (doğru/yanlış) değer. Varsayılan olarak False.
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Kullanıcının kayıt olduğu zaman. Varsayılan olarak şu anki UTC zamanı ile atanır.

    # Şifre Belirleme
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) # Kullanıcının girdiği düz şifreyi generate_password_hash fonksiyonu ile hash’ler ve password_hash alanına kaydeder.

    def check_password(self, password): # Kullanıcının giriş yaparken girdiği şifreyi hash’leyip, veri tabanındaki hash ile karşılaştırır.
        return check_password_hash(self.password_hash, password)
