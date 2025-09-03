#!/usr/bin/env python
import sqlite3
import os
from sqlite3 import Error
from prettytable import PrettyTable
import argparse
import hashlib
import datetime

# Veritabanı dosya yolu
DB_PATH = "instance/app.db"

def create_connection(db_path=DB_PATH):
    """Veritabanına bağlantı oluşturur"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(f"Veritabanına bağlanırken hata: {e}")
    
    return conn

def add_column_if_not_exists(column_name, column_type, db_path=DB_PATH):
    """Belirtilen sütun yoksa ekler"""
    conn = create_connection(db_path)
    
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Sütunun var olup olmadığını kontrol et
            cursor.execute("PRAGMA table_info(user)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if column_name not in columns:
                print(f"'{column_name}' sütunu ekleniyor...")
                cursor.execute(f"ALTER TABLE user ADD COLUMN {column_name} {column_type}")
                conn.commit()
                print(f"'{column_name}' sütunu başarıyla eklendi.")
            else:
                print(f"'{column_name}' sütunu zaten mevcut.")
                
        except Error as e:
            print(f"Sütun eklenirken hata: {e}")
        finally:
            conn.close()
    else:
        print("Veritabanına bağlanılamadı.")

def update_admin_status(email, is_admin=True, db_path=DB_PATH):
    """Belirtilen e-posta adresine sahip kullanıcının admin durumunu günceller"""
    conn = create_connection(db_path)
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # is_admin sütununun varlığını kontrol et
            add_column_if_not_exists("is_admin", "BOOLEAN DEFAULT 0", db_path)
            
            # Kullanıcının varlığını kontrol et
            cursor.execute("SELECT COUNT(*) FROM user WHERE email = ?", (email,))
            user_exists = cursor.fetchone()[0] > 0
            
            if user_exists:
                cursor.execute("UPDATE user SET is_admin = ? WHERE email = ?", (1 if is_admin else 0, email))
                conn.commit()
                print(f"'{email}' kullanıcısının admin durumu güncellendi: {'Admin' if is_admin else 'Normal Kullanıcı'}")
            else:
                print(f"'{email}' e-posta adresine sahip kullanıcı bulunamadı.")
                
            return user_exists
        except Error as e:
            print(f"Admin durumu güncellenirken hata: {e}")
            return False
        finally:
            conn.close()
    else:
        print("Veritabanına bağlanılamadı.")
        return False

def add_user(email, password, is_verified=False, is_admin=False, db_path=DB_PATH):
    """Yeni bir kullanıcı ekler"""
    conn = create_connection(db_path)
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Kullanıcının var olup olmadığını kontrol et
            cursor.execute("SELECT COUNT(*) FROM user WHERE email = ?", (email,))
            if cursor.fetchone()[0] > 0:
                print(f"'{email}' e-posta adresine sahip kullanıcı zaten mevcut.")
                return False
            
            # is_admin sütununun varlığını kontrol et
            add_column_if_not_exists("is_admin", "BOOLEAN DEFAULT 0", db_path)
            
            # Şifre hash'leme
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Tarih oluşturma
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Kullanıcı ekleme
            cursor.execute(
                "INSERT INTO user (email, password_hash, is_verified, created_at, is_admin) VALUES (?, ?, ?, ?, ?)",
                (email, password_hash, 1 if is_verified else 0, current_time, 1 if is_admin else 0)
            )
            conn.commit()
            print(f"'{email}' kullanıcısı başarıyla eklendi.")
            return True
            
        except Error as e:
            print(f"Kullanıcı eklenirken hata: {e}")
            return False
        finally:
            conn.close()
    else:
        print("Veritabanına bağlanılamadı.")
        return False

def show_users(db_path=DB_PATH):
    """Tüm kullanıcıları gösterir"""
    conn = create_connection(db_path)
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Tablodaki sütunları kontrol et
            cursor.execute("PRAGMA table_info(user)")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Kullanıcıları sorgula
            query = "SELECT id, email, is_verified, created_at"
            if "is_admin" in columns:
                query += ", is_admin"
            query += " FROM user"
            
            cursor.execute(query)
            users = cursor.fetchall()
            
            if users:
                # PrettyTable ile güzel görünümlü bir tablo oluştur
                table = PrettyTable()
                headers = ["ID", "Email", "Doğrulanmış", "Kayıt Tarihi"]
                if "is_admin" in columns:
                    headers.append("Admin")
                table.field_names = headers
                
                for user in users:
                    user_data = list(user)
                    user_data[2] = "Evet" if user_data[2] else "Hayır"
                    if "is_admin" in columns and len(user) > 4:
                        user_data[4] = "Evet" if user_data[4] else "Hayır"
                    table.add_row(user_data)
                
                print("\nKullanıcı Listesi:")
                print(table)
                print(f"\nToplam {len(users)} kullanıcı bulundu.")
            else:
                print("Veritabanında hiç kullanıcı bulunamadı.")
                
        except Error as e:
            print(f"Kullanıcılar listelenirken hata: {e}")
        finally:
            conn.close()
    else:
        print("Veritabanına bağlanılamadı.")

def main():
    parser = argparse.ArgumentParser(description="Veritabanı kullanıcı yönetim aracı")
    parser.add_argument("--db", "-d", default=DB_PATH, help="Veritabanı dosyasının yolu")
    
    subparsers = parser.add_subparsers(dest="command", help="Komut")
    
    # Kullanıcıları listeleme komutu
    list_parser = subparsers.add_parser("list", help="Kullanıcıları listele")
    
    # Admin yetkisi verme/alma komutu
    admin_parser = subparsers.add_parser("admin", help="Admin yetkisi ver/al")
    admin_parser.add_argument("email", help="Kullanıcı e-posta adresi")
    admin_parser.add_argument("--remove", "-r", action="store_true", help="Admin yetkisini kaldır")
    
    # Kullanıcı ekleme komutu
    add_parser = subparsers.add_parser("add", help="Yeni kullanıcı ekle")
    add_parser.add_argument("email", help="Kullanıcı e-posta adresi")
    add_parser.add_argument("password", help="Kullanıcı şifresi")
    add_parser.add_argument("--verified", "-v", action="store_true", help="Kullanıcıyı doğrulanmış olarak işaretle")
    add_parser.add_argument("--admin", "-a", action="store_true", help="Kullanıcıya admin yetkisi ver")
    
    args = parser.parse_args()
    
    # Komuta göre işlem yap
    if args.command == "list" or args.command is None:
        show_users(args.db)
    elif args.command == "admin":
        update_admin_status(args.email, not args.remove, args.db)
        show_users(args.db)
    elif args.command == "add":
        add_user(args.email, args.password, args.verified, args.admin, args.db)
        show_users(args.db)

if __name__ == "__main__":
    main()
