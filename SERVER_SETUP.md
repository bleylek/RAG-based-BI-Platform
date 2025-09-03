# Şirket Sunucusunda Kurulum Adımları

Bu talimatlar, RAG BI Platform'un şirket sunucunuzda (172.16.5.10) kurulumu için gerekli adımları içermektedir.

## 1. Sunucuya Bağlanma

```bash
ssh srvadmin@172.16.5.10
# Şifre: 123
```

## 2. Docker Kurulumu

Sunucuda Docker ve Docker Compose kurulu değilse:

```bash
# GitHub'dan kurulum scriptini indirin
wget https://raw.githubusercontent.com/bleylek/RAG-based-BI-Platform/master/install_docker.sh

# Scripti çalıştırılabilir yapın
chmod +x install_docker.sh

# Scripti çalıştırın
./install_docker.sh

# Oturumu kapatıp tekrar açın veya aşağıdaki komutu çalıştırın
newgrp docker
```

## 3. Uygulamayı Kurma

```bash
# GitHub'dan kurulum scriptini indirin
wget https://raw.githubusercontent.com/bleylek/RAG-based-BI-Platform/master/setup_server.sh

# Scripti çalıştırılabilir yapın
chmod +x setup_server.sh

# Scripti çalıştırın
./setup_server.sh
```

Script çalışırken:
- Sizden .env dosyasını düzenlemenizi isteyecek
- Admin kullanıcısı oluşturup oluşturmayacağınızı soracak
- Firewall ayarlarını yapmanızı hatırlatacak

## 4. Firewall Ayarları

Sunucunun dışından erişilebilir olmasını sağlamak için firewall ayarlarını yapın:

```bash
# Firewall'un durumunu kontrol edin
sudo ufw status

# Firewall aktif değilse etkinleştirin
sudo ufw enable

# 8080 portuna izin verin
sudo ufw allow 8080/tcp

# Ayarları uygulayın
sudo ufw reload
```

## 5. Erişim ve Test

Kurulum tamamlandıktan sonra, uygulamaya şu adreslerden erişebilirsiniz:
- Şirket içi ağdan: http://172.16.5.10:8080
- Sunucudan: http://localhost:8080

## 6. Uygulama Yönetimi

Uygulamayı yönetmek için:

```bash
# Logları görüntüleme
docker logs rag-bi-platform

# Uygulamayı yeniden başlatma
docker restart rag-bi-platform

# Uygulama durumunu kontrol etme
docker ps | grep rag-bi-platform

# Kullanıcıları listeleme
cd /opt/rag-bi-platform
python docker_users.py list
```

## 7. Sorun Giderme

Eğer uygulama çalışmazsa:

1. Docker servisinin çalıştığından emin olun:
   ```bash
   sudo systemctl status docker
   ```

2. Container'ın çalıştığını kontrol edin:
   ```bash
   docker ps | grep rag-bi-platform
   ```

3. Logları kontrol edin:
   ```bash
   docker logs rag-bi-platform
   ```

4. Servis durumunu kontrol edin:
   ```bash
   sudo systemctl status rag-bi-platform
   ```

5. Firewall ayarlarını kontrol edin:
   ```bash
   sudo ufw status
   ```

## 8. Güncelleme

Uygulamayı güncellemek için:

```bash
cd /opt/rag-bi-platform
git pull
docker-compose down
docker-compose up -d --build
```
