# RAG BI Platform

RAG (Retrieval Augmented Generation) tabanlı, iş dünyası için özel tasarlanmış bir karar destek platformu.

## Özellikler

- CV Karşılaştırma ve Analizi
- Teklif Karşılaştırma
- Sözleşme Karşılaştırma ve Analizi
- Mail/Mesaj Oluşturucu
- RAG Teknolojisi (Yüzlerce dosya ile çalışabilme)
- Kullanıcı Kimlik Doğrulama ve Yetkilendirme

## Teknoloji Yığını

- **Backend**: Flask 3.0
- **Veritabanı**: SQLAlchemy (SQLite/PostgreSQL)
- **Yapay Zeka**: OpenAI API (GPT-4)
- **Vektör Veritabanı**: FAISS
- **Embeddings**: Sentence Transformers
- **Kimlik Doğrulama**: Argon2, Email Doğrulama
- **Frontend**: HTML/CSS/JS, Jinja2 Templates
- **Deployment**: Docker, Gunicorn

## Kurulum

### Gereksinimler

- Python 3.10+
- Docker ve Docker Compose (Docker ile kurulum için)
- OpenAI API Anahtarı

### Yerel Kurulum

1. Repository'yi klonlayın:
   ```
   git clone https://github.com/bleylek/RAG-based-BI-Platform.git
   cd RAG-based-BI-Platform
   ```

2. Sanal ortam oluşturun ve etkinleştirin:
   ```
   python -m venv venv
   
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows Command Prompt
   venv\Scripts\activate.bat
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. Bağımlılıkları yükleyin:
   ```
   pip install -r requirements.txt
   ```

4. `.env.example` dosyasını `.env` olarak kopyalayın ve değerlerinizi ayarlayın:
   ```
   # Windows PowerShell
   Copy-Item .env.example -Destination .env
   
   # Linux/Mac
   cp .env.example .env
   
   # Dosyayı düzenleyin ve gerekli API anahtarlarını ekleyin
   ```

5. Uygulamayı çalıştırın:
   ```
   python run.py
   ```

### Docker ile Kurulum (Önerilen)

1. Repository'yi klonlayın:
   ```
   git clone https://github.com/bleylek/RAG-based-BI-Platform.git
   cd RAG-based-BI-Platform
   ```

2. Sağlanan build scriptini kullanarak Docker ortamını oluşturun:

   **Windows PowerShell:**
   ```
   # Otomatik kurulum ve çalıştırma
   .\docker-build.ps1
   
   # VEYA Docker yönetim scriptini kullanarak
   .\docker-manage.ps1 start
   ```

   **Linux/Mac:**
   ```
   # Docker Compose ile direkt başlatma
   docker compose up -d
   ```

## Kullanıcı Yönetimi

Platform, kullanıcı hesaplarını yerel SQLite veritabanında saklar. Kullanıcıları görüntülemek ve yönetmek için aşağıdaki araçları kullanabilirsiniz:

### Yerel Kullanıcı Yönetimi

Yerel geliştirme ortamında çalışırken:

```bash
# Tüm kullanıcıları listele
python list_users.py

# Kullanıcı ekle (doğrulanmış ve admin olarak)
python update_db.py add admin@example.com password123 --verified --admin

# Admin yetkisi ver/al
python update_db.py admin user@example.com  # Admin yetkisi ver
python update_db.py admin user@example.com --remove  # Admin yetkisini kaldır
```

### Docker Kullanıcı Yönetimi

Docker container'ında çalışırken:

```bash
# Tüm kullanıcıları listele
python docker_users.py list

# Belirli bir container'daki kullanıcıları listele
python docker_users.py --container [CONTAINER_ID] list

# Yeni kullanıcı ekle
python docker_users.py add user@example.com password123 --verified

# Admin yetkisi ver/al
python docker_users.py admin user@example.com  # Admin yetkisi ver
python docker_users.py admin user@example.com --remove  # Admin yetkisini kaldır
```

3. Tarayıcınızdan `http://localhost:8080` adresine gidin

## Docker Yönetim Araçları

Uygulama için çeşitli Docker yönetim scriptleri sağlanmıştır:

- **docker-build.ps1**: Optimizasyonlar ile Docker imajını oluşturur ve başlatır
- **docker-cleanup.ps1**: Docker kaynaklarını temizleyerek disk alanı kazandırır
- **docker-manage.ps1**: Temel konteyner yönetimi için yardımcı araç

Yönetim scripti kullanımı:
```powershell
# Konteyner durumunu göster
.\docker-manage.ps1 status

# Konteyneri başlat
.\docker-manage.ps1 start

# Konteyneri durdur
.\docker-manage.ps1 stop

# Logları görüntüle
.\docker-manage.ps1 logs
```

## Docker Optimizasyonları

Bu proje, performans ve güvenilirlik için çeşitli Docker optimizasyonları içerir:

- **Multi-stage builds**: Daha küçük final imaj boyutu için
- **Layer caching**: Daha hızlı build süreleri için akıllı katmanlama
- **Health checks**: Uygulamanın durumunu izlemek için
- **Volume mounts**: Veri kalıcılığı için
- **Resource limits**: Sistem kaynaklarını yönetmek için
- **Non-root user**: Güvenlik için düşük yetkili kullanıcı

## Kullanım

1. Kayıt olun ve email doğrulamasını tamamlayın
2. Giriş yapın
3. Ana sayfadan istediğiniz modülü seçin:
   - CV Karşılaştırma ve Analizi
   - Teklif Karşılaştırma ve Sıralama
   - Sözleşme Karşılaştırma ve Analizi
   - Mail/Mesaj Oluşturma ve Düzenleme

## Docker Sorun Giderme

Eğer Docker kurulumunda sorunlarla karşılaşıyorsanız:

1. Docker servisinin çalıştığından emin olun
2. Temiz bir build için `docker-cleanup.ps1` scriptini çalıştırın
3. Logları kontrol edin: `docker compose logs`
4. Sistem kaynaklarınızın yeterli olduğundan emin olun (özellikle bellek)
5. Docker disk alanı kullanımını kontrol edin: `docker system df`

## Geliştirme

1. Değişikliklerinizi yapın
2. Geliştirme ortamında test edin
3. Docker ile test edin: `.\docker-build.ps1`
4. Pull request gönderin

## Lisans

Bu proje [LICENSE](LICENSE) lisansı altında lisanslanmıştır.

## İletişim

- Github: [bleylek](https://github.com/bleylek)
