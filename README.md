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
- **Deployment**: Gunicorn

## Kurulum

### Gereksinimler

- Python 3.10+
- OpenAI API Anahtarı

### Kurulum

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

### Sunucuda Sürekli Çalışma

Uygulamanın sunucuda sürekli çalışması için:

1. Systemd servisi oluşturun ve başlatın:
   ```bash
   sudo cp rag-bi-platform.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable rag-bi-platform
   sudo systemctl start rag-bi-platform
   ```

Daha detaylı bilgi için `CONTINUOUS_RUNNING.md` dosyasını inceleyebilirsiniz.

## Kullanıcı Yönetimi

Platform, kullanıcı hesaplarını yerel SQLite veritabanında saklar. Kullanıcıları görüntülemek ve yönetmek için aşağıdaki araçları kullanabilirsiniz:

### Kullanıcı Yönetimi

```bash
# Tüm kullanıcıları listele
python list_users.py

# Kullanıcı ekle (opsiyonel olarak doğrulanmış)
python create_user.py user@example.com password123 --verified
```

## Uygulama Erişimi

Uygulama çalıştırıldıktan sonra tarayıcınızdan `http://localhost:5000` adresine giderek erişebilirsiniz.

## Kullanım

1. Kayıt olun ve email doğrulamasını tamamlayın
2. Giriş yapın
3. Ana sayfadan istediğiniz modülü seçin:
   - CV Karşılaştırma ve Analizi
   - Teklif Karşılaştırma ve Sıralama
   - Sözleşme Karşılaştırma ve Analizi
   - Mail/Mesaj Oluşturma ve Düzenleme

## Geliştirme

1. Değişikliklerinizi yapın
2. Geliştirme ortamında test edin
3. Pull request gönderin

## Lisans

Bu proje [LICENSE](LICENSE) lisansı altında lisanslanmıştır.

## İletişim

- Github: [bleylek](https://github.com/bleylek)
