#!/usr/bin/env python
# create_user.py - Yeni kullanıcı oluşturma scripti

import os
import sys
import argparse
from werkzeug.security import generate_password_hash
from datetime import datetime
import sqlite3

def create_user(email, password, verified=False, db_path="instance/app.db"):
    """Yeni kullanıcı oluştur"""
    
    # Veritabanı dizini yoksa oluştur
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Kullanıcı tablosu oluştur (yoksa)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password_hash TEXT,
                is_verified BOOLEAN,
                created_at TEXT
            )
        ''')
        
        # Kullanıcının var olup olmadığını kontrol et
        cursor.execute('SELECT COUNT(*) FROM user WHERE email = ?', (email,))
        if cursor.fetchone()[0] > 0:
            print(f"Hata: {email} e-posta adresi ile kullanıcı zaten mevcut.")
            return False
        
        # Kullanıcı oluştur
        password_hash = generate_password_hash(password)
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO user (email, password_hash, is_verified, created_at) 
            VALUES (?, ?, ?, ?)
        ''', (email, password_hash, verified, created_at))
        
        conn.commit()
        print(f"Kullanıcı başarıyla oluşturuldu: {email}")
        return True
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Yeni kullanıcı oluştur')
    parser.add_argument('email', help='Kullanıcı email adresi')
    parser.add_argument('password', help='Kullanıcı şifresi')
    parser.add_argument('--verified', action='store_true', help='Email doğrulanmış olarak işaretle')
    
    args = parser.parse_args()
    
    create_user(args.email, args.password, args.verified)
