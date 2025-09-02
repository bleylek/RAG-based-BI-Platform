FROM python:3.10-slim

WORKDIR /app

# Sistem bağımlılıklarını yükleyin
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    libpq-dev \
    poppler-utils \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyalayın ve yükleyin
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyalayın
COPY . .

# Gerekli dizinleri oluşturun
RUN mkdir -p rag_store/uploads

# Docker içinde çalışacak kullanıcı oluşturun (güvenlik için)
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Uygulama portu
EXPOSE 5000

# Çalıştırma komutu
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
