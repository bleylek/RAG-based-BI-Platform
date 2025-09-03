#!/bin/bash
# setup_server.sh - RAG BI Platform'un sunucuda kurulumu için script

echo "RAG BI Platform kurulumu başlatılıyor..."

# Git kurulu mu kontrol et
if ! command -v git &> /dev/null
then
    echo "Git kuruluyor..."
    sudo apt-get update
    sudo apt-get install -y git
fi

# Uygulama dizini
APP_DIR="/opt/rag-bi-platform"

# Uygulama dizinini oluştur
echo "Uygulama dizini oluşturuluyor: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# GitHub'dan projeyi klonla
echo "GitHub'dan proje klonlanıyor..."
git clone https://github.com/bleylek/RAG-based-BI-Platform.git $APP_DIR

# Çalışma dizinine geç
cd $APP_DIR

# .env dosyasını oluştur
echo "Çevre değişkenleri dosyası oluşturuluyor..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Lütfen .env dosyasını düzenleyerek gerekli API anahtarlarını ekleyin:"
    echo "nano $APP_DIR/.env"
fi

# Docker Compose ile uygulamayı başlat
echo "Docker Compose ile uygulama başlatılıyor..."
docker-compose up -d

# Systemd servisi oluştur
echo "Systemd servisi kuruluyor..."
cat > /tmp/rag-bi-platform.service << EOF
[Unit]
Description=RAG BI Platform Docker Compose Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$APP_DIR
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

sudo mv /tmp/rag-bi-platform.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rag-bi-platform
sudo systemctl start rag-bi-platform

# Admin kullanıcısı oluştur
echo "Admin kullanıcısı oluşturmak ister misiniz? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Admin e-posta adresi:"
    read -r admin_email
    echo "Admin şifresi:"
    read -rs admin_password
    echo
    bash $APP_DIR/init_container.sh "$admin_email" "$admin_password"
fi

# IP adresini al
IP_ADDRESS=$(hostname -I | awk '{print $1}')

echo "Kurulum tamamlandı!"
echo "Uygulamaya şu adresten erişebilirsiniz: http://$IP_ADDRESS:8080"
echo "Firewall'da 8080 portunu açmayı unutmayın: sudo ufw allow 8080/tcp"
