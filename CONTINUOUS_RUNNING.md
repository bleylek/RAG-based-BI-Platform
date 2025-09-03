# Sürekli Çalışma Kurulum Talimatları

Bu talimatlar, RAG BI Platform'un sunucuda sürekli çalışmasını sağlamak için gerekli adımları içerir.

## Systemd Service ile Sürekli Çalışma

1. Bu depodaki `rag-bi-platform.service` dosyasını düzenleyerek doğru çalışma dizininizi belirtin:
   
   ```bash
   sudo nano /etc/systemd/system/rag-bi-platform.service
   ```

   WorkingDirectory satırını gerçek çalışma dizininizle güncelleyin:
   ```
   WorkingDirectory=/path/to/RAG-based-BI-Platform
   ```

2. Servis dosyasını `/etc/systemd/system/` dizinine kopyalayın:

   ```bash
   sudo cp rag-bi-platform.service /etc/systemd/system/
   ```

3. Systemd'yi yeniden yükleyin:

   ```bash
   sudo systemctl daemon-reload
   ```

4. Servisi etkinleştirin ve başlatın:

   ```bash
   sudo systemctl enable rag-bi-platform
   sudo systemctl start rag-bi-platform
   ```

5. Servisin durumunu kontrol edin:

   ```bash
   sudo systemctl status rag-bi-platform
   ```

## Docker'ın Otomatik Başlaması

Docker'ın sistem başlangıcında otomatik başlamasını sağlamak için:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

## Konteyner Yeniden Başlatma İlkesi

Bu projedeki docker-compose.yml dosyasında `restart: always` parametresi zaten yapılandırılmıştır. Bu, konteyner çöktüğünde veya sunucu yeniden başlatıldığında, konteynerinizin otomatik olarak yeniden başlatılmasını sağlar.

## Güvenlik ve Güncellemeler

1. Düzenli güncelleme için bir cron işi ekleyin:

   ```bash
   sudo crontab -e
   ```

   Ve şu satırı ekleyin (haftalık olarak güncellemek için):
   
   ```
   0 2 * * 0 cd /path/to/RAG-based-BI-Platform && git pull && docker-compose down && docker-compose up -d
   ```

2. Düzenli yedekleme için bir cron işi ekleyin:

   ```bash
   0 3 * * * cd /path/to/RAG-based-BI-Platform && docker exec rag-bi-platform sh -c "sqlite3 instance/app.db .dump" > /backup/rag_backup_$(date +\%Y-\%m-\%d).sql
   ```

## İzleme ve Uyarılar

Sürekli çalışma için izleme sistemi kurabilirsiniz:

1. Basit izleme için:
   ```bash
   sudo apt-get install monit
   ```

2. Monit yapılandırması:
   ```
   check host rag-bi-platform with address 127.0.0.1
      start program = "/usr/bin/docker start rag-bi-platform"
      stop program = "/usr/bin/docker stop rag-bi-platform"
      if failed port 8080 protocol http for 3 cycles then restart
   ```

Bu adımları takip ederek uygulamanız sunucuda kesintisiz çalışacaktır.
