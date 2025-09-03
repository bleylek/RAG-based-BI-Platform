#!/bin/bash
# install_docker.sh - Docker ve Docker Compose kurulumu için script

echo "Docker ve Docker Compose kurulumu başlatılıyor..."

# Güvenlik için çalışmadan önce onay al
read -p "Docker ve Docker Compose kurulumu başlatılsın mı? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Kurulum iptal edildi."
    exit 1
fi

# Gerekli paketlerin kurulumu
echo "Gerekli paketler kuruluyor..."
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg

# Docker'ın GPG anahtarını ekleyin
echo "Docker GPG anahtarı ekleniyor..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Docker deposunu ekleyin
echo "Docker deposu ekleniyor..."
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Docker'ı kurun
echo "Docker kuruluyor..."
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Kullanıcıyı docker grubuna ekleyin (sudo olmadan docker komutlarını çalıştırmak için)
echo "Kullanıcı docker grubuna ekleniyor..."
sudo usermod -aG docker $USER

# Docker Compose'u kurun
echo "Docker Compose kuruluyor..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Docker servisini etkinleştirin ve başlatın
echo "Docker servisi etkinleştiriliyor ve başlatılıyor..."
sudo systemctl enable docker
sudo systemctl start docker

echo "Docker ve Docker Compose kurulumu tamamlandı!"
echo "Lütfen oturumu kapatıp tekrar açın veya 'newgrp docker' komutunu çalıştırın."
echo "Docker sürümü:"
docker --version
echo "Docker Compose sürümü:"
docker-compose --version
