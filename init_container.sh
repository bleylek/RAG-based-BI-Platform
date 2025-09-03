#!/bin/bash
# init_container.sh - Docker container ilk çalıştırıldığında yapılması gereken işlemler
# Bu script ilk kullanıcı oluşturma ve diğer başlangıç işlemleri için kullanılabilir

# Kullanımı: ./init_container.sh admin@example.com admin_password

set -e

if [ $# -lt 2 ]; then
    echo "Kullanımı: $0 <admin_email> <admin_password>"
    exit 1
fi

ADMIN_EMAIL=$1
ADMIN_PASSWORD=$2
CONTAINER_NAME="rag-bi-platform"

# Container çalıştığını kontrol et
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "Hata: $CONTAINER_NAME container'ı çalışmıyor!"
    echo "Önce container'ı başlatın: docker-compose up -d"
    exit 1
fi

echo "Container içinde admin kullanıcısı oluşturuluyor..."

# Admin kullanıcısı oluşturma
docker exec $CONTAINER_NAME python -c "
import sqlite3
import hashlib
import datetime

# Veritabanına bağlantı
conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()

# Kullanıcının var olup olmadığını kontrol et
cursor.execute('SELECT COUNT(*) FROM user WHERE email = ?', ('$ADMIN_EMAIL',))
if cursor.fetchone()[0] == 0:
    # is_admin sütununun varlığını kontrol et
    cursor.execute('PRAGMA table_info(user)')
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'is_admin' not in columns:
        cursor.execute('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0')
        print('is_admin sütunu eklendi')

    # Admin kullanıcısı oluştur
    password_hash = hashlib.sha256('$ADMIN_PASSWORD'.encode()).hexdigest()
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO user (email, password_hash, is_verified, created_at, is_admin) 
        VALUES (?, ?, 1, ?, 1)
    ''', ('$ADMIN_EMAIL', password_hash, created_at))
    
    conn.commit()
    print('Admin kullanıcısı oluşturuldu: $ADMIN_EMAIL')
else:
    # Admin yetkisi ver
    cursor.execute('UPDATE user SET is_verified = 1, is_admin = 1 WHERE email = ?', ('$ADMIN_EMAIL',))
    conn.commit()
    print('$ADMIN_EMAIL kullanıcısı güncellendi (Admin yetkisi verildi)')

conn.close()
"

echo "İşlem tamamlandı!"
echo "Artık RAG BI Platform'a $ADMIN_EMAIL kullanıcısı ile giriş yapabilirsiniz."
