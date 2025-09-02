# app/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session # Blueprint: Flask içinde modüler yapı kurmamıza olanak tanır. flash: Kullanıcıya mesaj göstermek için kullanılır. session: Giriş yapan kullanıcının bilgilerini (örneğin user_id) geçici olarak saklar.
from app.auth.models import db, User
from app.auth.utils import send_verification_email, generate_token, verify_token # utils.py dosyasındaki token üretme, e-posta gönderme ve token doğrulama fonksiyonları kullanılır.

from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint tanımı
auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # auth_bp: Bu Blueprint'e ait route'lar /auth/... ile başlar (örneğin /auth/login).

# Kullanıcı Kayıt – /auth/register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email.endswith("@control-ix.com"):
            flash("Sadece control-ix.com uzantılı adreslerle kayıt olunabilir.", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first(): # Aynı e-posta ile önceden kayıt olunup olunmadığı kontrol edilir.
            flash("Bu e-posta ile zaten kayıtlı bir kullanıcı var.", "warning")
            return redirect(url_for('auth.register'))

        user = User(email=email)
        user.set_password(password) # Yeni kullanıcı oluşturulur, şifre hash’lenir.
        db.session.add(user)
        db.session.commit()
        
        # Token oluştur ve e-posta gönder
        token = generate_token(email)
        send_verification_email(email, token) # Veritabanına eklenir ve e-posta doğrulama linki gönderilir.
        
        flash("Kayıt başarılı! Lütfen e-postanızı doğrulayın.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# Kullanıcı Giriş – /auth/login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first() # E-posta veritabanında aranır.

        if not user or not user.check_password(password): # Kullanıcı yoksa veya şifre eşleşmiyorsa hata mesajı verilir.
            flash("E-posta veya şifre hatalı.", "danger")
            return redirect(url_for('auth.login'))

        if not user.is_verified: # E-posta doğrulaması yapılmadıysa girişe izin verilmez.
            flash("Lütfen önce e-posta adresinizi doğrulayın.", "warning")
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id # Giriş başarılı ise kullanıcının id'si oturumda saklanır.
        flash("Giriş başarılı!", "success")
        return redirect(url_for('main.index'))  # Ana sayfaya yönlendirme

    return render_template('login.html') # GET aşaması, giriş formu gösterilir


# E-Posta Doğrulama – /auth/verify/<token>
@auth_bp.route('/verify/<token>')
def verify_email(token):
    email = verify_token(token) # URL'deki token çözülerek e-posta bilgisi alınır.
    if not email:
        flash("Geçersiz veya süresi dolmuş doğrulama bağlantısı.", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for('auth.register'))

    user.is_verified = True
    db.session.commit() # Kullanıcı doğrulanır ve is_verified alanı True yapılır.
    flash("E-posta başarıyla doğrulandı. Giriş yapabilirsiniz.", "success")
    return redirect(url_for('auth.login'))

# Çıkış – /auth/logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for('auth.login'))
