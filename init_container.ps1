#!/usr/bin/env pwsh
# init_container.ps1 - Docker container ilk çalıştırıldığında yapılması gereken işlemler
# Bu script ilk kullanıcı oluşturma ve diğer başlangıç işlemleri için kullanılabilir

param (
    [Parameter(Mandatory=$true)]
    [string]$AdminEmail,
    
    [Parameter(Mandatory=$true)]
    [string]$AdminPassword
)

$ContainerName = "rag-bi-platform"

# Container çalıştığını kontrol et
$containerRunning = docker ps | Select-String -Pattern $ContainerName
if (-not $containerRunning) {
    Write-Host "Hata: $ContainerName container'ı çalışmıyor!" -ForegroundColor Red
    Write-Host "Önce container'ı başlatın: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

Write-Host "Container içinde admin kullanıcısı oluşturuluyor..." -ForegroundColor Cyan

# Python scripti oluştur (özel karakterlerin düzgün çalışması için)
$pythonScript = @"
import sqlite3
import hashlib
import datetime

# Veritabanına bağlantı
conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()

# Kullanıcının var olup olmadığını kontrol et
cursor.execute('SELECT COUNT(*) FROM user WHERE email = ?', ('$AdminEmail',))
if cursor.fetchone()[0] == 0:
    # is_admin sütununun varlığını kontrol et
    cursor.execute('PRAGMA table_info(user)')
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'is_admin' not in columns:
        cursor.execute('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0')
        print('is_admin sütunu eklendi')

    # Admin kullanıcısı oluştur
    password_hash = hashlib.sha256('$AdminPassword'.encode()).hexdigest()
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO user (email, password_hash, is_verified, created_at, is_admin) 
        VALUES (?, ?, 1, ?, 1)
    ''', ('$AdminEmail', password_hash, created_at))
    
    conn.commit()
    print('Admin kullanıcısı oluşturuldu: $AdminEmail')
else:
    # Admin yetkisi ver
    cursor.execute('UPDATE user SET is_verified = 1, is_admin = 1 WHERE email = ?', ('$AdminEmail',))
    conn.commit()
    print('$AdminEmail kullanıcısı güncellendi (Admin yetkisi verildi)')

conn.close()
"@

# Python scriptini container içinde çalıştır
$pythonScript = $pythonScript -replace '"', '\"'
$command = "docker exec $ContainerName python -c `"$pythonScript`""
Invoke-Expression $command

Write-Host "`nİşlem tamamlandı!" -ForegroundColor Green
Write-Host "Artık RAG BI Platform'a $AdminEmail kullanıcısı ile giriş yapabilirsiniz." -ForegroundColor Green
