# app/auth/utils.py

from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Token oluşturucu
def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="email-confirm-salt")

# Token doğrulayıcı
def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt="email-confirm-salt", max_age=expiration)
        return email

    except Exception:
        return None
# Doğrulama maili gönderici
def send_verification_email(email, token):
    confirm_url = url_for("auth.verify_email", token=token, _external=True)
    subject = "Controlix BI – E-posta Doğrulama"
    body = f"""Merhaba,
Controlix BI platformuna kaydolduğunuz için teşekkür ederiz.
Hesabınızı doğrulamak için aşağıdaki bağlantıya tıklayın:

{confirm_url}

Bu bağlantı 1 saat içinde geçerliliğini yitirecektir.

İyi çalışmalar,
Controlix BI Ekibi
"""
     # Mail ayarları
    smtp_server = current_app.config["MAIL_SERVER"]
    smtp_port = current_app.config["MAIL_PORT"]
    smtp_user = current_app.config["MAIL_USERNAME"]
    smtp_password = current_app.config["MAIL_PASSWORD"]
    sender_email = current_app.config["MAIL_USERNAME"]

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            print(f"[+] Doğrulama e-postası gönderildi: {email}")
    except Exception as e:
        print(f"[!] E-posta gönderim hatası: {e}")