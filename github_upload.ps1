# Bu betik, projeyi GitHub'a yüklemek için gerekli git komutlarını içerir
# KULLANIM: Bu dosyayı PowerShell ile çalıştırın veya komutları kopyalayıp PowerShell'de çalıştırın

# 1. Git reposunu başlatın
git init

# 2. Tüm dosyaları git izleme listesine ekleyin
git add .

# 3. İlk commit'i oluşturun
git commit -m "Initial commit: RAG-based BI Platform"

# 4. GitHub reponuzu uzak repo olarak ayarlayın
# NOT: Halihazırda bir remote varsa, önce kaldırıp yeniden ekliyoruz
git remote remove origin
git remote add origin https://github.com/bleylek/RAG-based-BI-Platform.git

# 5. Yerel repo'yu GitHub'a gönderin
git branch -M master
git push -u origin master

Write-Host "Proje başarıyla GitHub'a yüklendi!" -ForegroundColor Green
