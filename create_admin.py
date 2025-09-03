#!/usr/bin/env python

# Bu script interaktif bir admin kullanıcısı oluşturmak için kullanılır
import os
import sys
import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime
import argparse

def create_admin_user(email, password, db_path="instance/app.db"):
    """Admin kullanıcısı oluştur"""
    
    # DB varsa bağlan, yoksa çık
    if not os.path.exists(db_path):
        print(f"Hata: Veritabanı bulunamadı: {db_path}")
        return False
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Kullanıcı zaten var mı kontrol et
        cursor.execute("SELECT id FROM user WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            # Kullanıcıyı admin yap
            cursor.execute("UPDATE user SET is_verified = 1 WHERE email = ?", (email,))
            print(f"Kullanıcı '{email}' zaten mevcut. Admin yetkisi verildi.")
        else:
            # Yeni admin kullanıcısı oluştur
            hash_pw = generate_password_hash(password)
            now = datetime.utcnow()
            
            # is_admin kolon kontrolü
            cursor.execute("PRAGMA table_info(user)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if "is_admin" in columns:
                cursor.execute(
                    "INSERT INTO user (email, password_hash, is_verified, created_at, is_admin) VALUES (?, ?, 1, ?, 1)",
                    (email, hash_pw, now)
                )
            else:
                cursor.execute(
                    "INSERT INTO user (email, password_hash, is_verified, created_at) VALUES (?, ?, 1, ?)",
                    (email, hash_pw, now)
                )
            
            print(f"Yeni admin kullanıcısı oluşturuldu: {email}")
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Hata oluştu: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Admin kullanıcısı oluştur")
    parser.add_argument("--email", "-e", required=True, help="Admin e-posta adresi")
    parser.add_argument("--password", "-p", required=True, help="Admin parolası")
    parser.add_argument("--db", "-d", default="instance/app.db", help="Veritabanı yolu")
    
    args = parser.parse_args()
    
    if create_admin_user(args.email, args.password, args.db):
        print("İşlem başarıyla tamamlandı.")
        sys.exit(0)
    else:
        print("İşlem başarısız oldu.")
        sys.exit(1)
