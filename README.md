# Controlix BI Platform

RAG (Retrieval Augmented Generation) tabanlı, iş dünyası için özel tasarlanmış bir karar destek platformu.

## Özellikler

- CV Karşılaştırma ve Analizi
- Teklif Karşılaştırma
- Sözleşme Karşılaştırma ve Analizi
- Mail/Mesaj Oluşturucu
- RAG Teknolojisi (Yüzlerce dosya ile çalışabilme)
- Kullanıcı Kimlik Doğrulama ve Yetkilendirme

## Teknoloji Yığını

- **Backend**: Flask
- **Veritabanı**: SQLAlchemy (SQLite/PostgreSQL)
- **Yapay Zeka**: OpenAI GPT-4
- **Vektör Veritabanı**: FAISS
- **Kimlik Doğrulama**: JWT, Email Doğrulama
- **Frontend**: HTML/CSS/JS

## Kurulum

### Gereksinimler

- Python 3.8+
- Docker ve Docker Compose (isteğe bağlı)

### Yerel Kurulum

1. Repository'yi klonlayın:
   ```
   git clone https://github.com/username/controlix-bi.git
   cd controlix-bi
   ```

2. Sanal ortam oluşturun ve etkinleştirin:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Bağımlılıkları yükleyin:
   ```
   pip install -r requirements.txt
   ```

4. `.env.example` dosyasını `.env` olarak kopyalayın ve değerlerinizi ayarlayın:
   ```
   cp .env.example .env
   # Dosyayı düzenleyin ve gerekli API anahtarlarını ekleyin
   ```

5. Uygulamayı çalıştırın:
   ```
   python run.py
   ```

### Docker ile Kurulum

1. Repository'yi klonlayın:
   ```
   git clone https://github.com/username/controlix-bi.git
   cd controlix-bi
   ```

2. `.env.example` dosyasını `.env` olarak kopyalayın ve değerlerinizi ayarlayın:
   ```
   cp .env.example .env
   # Dosyayı düzenleyin ve gerekli API anahtarlarını ekleyin
   ```

3. Docker Compose ile çalıştırın:
   ```
   docker-compose up -d
   ```

4. Tarayıcınızdan `http://localhost:5000` adresine gidin

## Kullanım

1. Kayıt olun ve email doğrulamasını tamamlayın
2. Giriş yapın
3. Ana sayfadan istediğiniz modülü seçin:
   - CV Karşılaştırma
   - Teklif Karşılaştırma
   - Sözleşme Karşılaştırma
   - Mail/Mesaj Oluşturucu

## Geliştirme

1. Değişikliklerinizi yapın
2. Test edin: `pytest`
3. Pull request gönderin

## Lisans

Bu proje [LICENSE](LICENSE) lisansı altında lisanslanmıştır.

## İletişim

- Şirket: [Controlix](https://example.com)
- Email: info@example.com
