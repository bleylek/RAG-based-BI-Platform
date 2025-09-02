# Bu betik, projeyi GitHub'a yüklemek için gerekli git komutlarını içerir
# KULLANIM: Bu dosyayı PowerShell ile çalıştırın veya komutları kopyalayıp PowerShell'de çalıştırın

# 1. Git reposunu başlatın
git init

# 2. Tüm dosyaları git izleme listesine ekleyin
git add .

# 3. İlk commit'i oluşturun
git commit -m "Initial commit: RAG-based BI Platform"

# 4. GitHub reponuzu uzak repo olarak ekleyin
# NOT: Aşağıdaki URL'yi kendi GitHub repo URL'nizle değiştirin
git remote add origin https://github.com/username/controlix-bi.git

# 5. Yerel repo'yu GitHub'a gönderin
git branch -M main
git push -u origin main

Write-Host "Projeniz başarıyla GitHub'a yüklendi!" -ForegroundColor Green
