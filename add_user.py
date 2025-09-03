import sqlite3

def create_user(email, password, is_verified=True, is_admin=False):
    from werkzeug.security import generate_password_hash
    
    # SQLite veritabanına bağlan
    conn = sqlite3.connect('instance/app.db')
    cursor = conn.cursor()
    
    # Kullanıcının var olup olmadığını kontrol et
    cursor.execute('SELECT id FROM user WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    if user:
        print(f"'{email}' e-posta adresi zaten kullanılıyor.")
    else:
        # Kullanıcı oluştur
        password_hash = generate_password_hash(password)
        from datetime import datetime
        now = datetime.utcnow()
        
        cursor.execute(
            'INSERT INTO user (email, password_hash, is_verified, created_at, is_admin) VALUES (?, ?, ?, ?, ?)',
            (email, password_hash, 1 if is_verified else 0, now, 1 if is_admin else 0)
        )
        
        conn.commit()
        print(f"Kullanıcı oluşturuldu: {email}")
    
    # Kullanıcıları listele
    cursor.execute('SELECT id, email, is_verified, is_admin FROM user')
    users = cursor.fetchall()
    
    print("\nKullanıcı Listesi:")
    print("=" * 60)
    print(f"{'ID':<5} {'Email':<30} {'Doğrulanmış':<12} {'Admin':<5}")
    print("-" * 60)
    
    for user in users:
        user_id, email, is_verified, is_admin = user
        print(f"{user_id:<5} {email:<30} {bool(is_verified):<12} {bool(is_admin):<5}")
    
    conn.close()

if __name__ == '__main__':
    # Normal kullanıcı oluştur
    create_user('user@example.com', 'user123', is_verified=True, is_admin=False)
