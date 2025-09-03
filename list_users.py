#!/usr/bin/env python
# list_users.py
import sqlite3
import os
from prettytable import PrettyTable

def list_users(db_path="instance/app.db"):
    """Veritabanındaki kullanıcıları listeler"""
    
    if not os.path.exists(db_path):
        print(f"Hata: Veritabanı bulunamadı: {db_path}")
        print(f"Mevcut dizin: {os.getcwd()}")
        print(f"Mevcut dizindeki dosyalar: {os.listdir()}")
        if os.path.exists("instance"):
            print(f"instance dizinindeki dosyalar: {os.listdir('instance')}")
        return
    
    try:
        # SQLite veritabanına bağlanma
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Tablonun yapısını kontrol et
        cursor.execute("PRAGMA table_info(user)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Kullanıcıları sorgula
        query = "SELECT id, email, is_verified, created_at"
        query += " FROM user"
        
        cursor.execute(query)
        users = cursor.fetchall()
        
        if users:
            # PrettyTable ile güzel görünümlü bir tablo oluştur
            user_table = PrettyTable()
            headers = ["ID", "Email", "Doğrulanmış", "Kayıt Tarihi"]
            user_table.field_names = headers
            
            for user in users:
                user_data = list(user)
                user_data[2] = "Evet" if user_data[2] else "Hayır"
                user_table.add_row(user_data)
            
            print("\nKullanıcı Listesi:")
            print(user_table)
            print(f"\nToplam {len(users)} kullanıcı bulundu.")
        else:
            print("Veritabanında hiç kullanıcı bulunmamaktadır.")
        
        # Tablonun yapısını gösterme
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        
        structure_table = PrettyTable()
        structure_table.field_names = ["Sıra", "Kolon Adı", "Tip", "Not Null", "Varsayılan", "Primary Key"]
        
        for col in columns:
            cid, name, type, notnull, dflt_value, pk = col
            structure_table.add_row([cid, name, type, bool(notnull), dflt_value, bool(pk)])
        
        print("\nUser Tablosu Yapısı:")
        print(structure_table)
        
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Veritabanındaki kullanıcıları listeler")
    parser.add_argument("--db", "-d", default="instance/app.db", help="Veritabanı dosyasının yolu")
    args = parser.parse_args()
    
    list_users(args.db)
