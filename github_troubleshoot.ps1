# GitHub push hataları için sorun giderme betiği

Write-Host "GitHub Push Sorun Giderici" -ForegroundColor Cyan
Write-Host "------------------------" -ForegroundColor Cyan

# Git durumunu kontrol et
Write-Host "Git Durumu:" -ForegroundColor Yellow
git status

# Remote'ları kontrol et
Write-Host "`nRemote Repolar:" -ForegroundColor Yellow
git remote -v

# GitHub'a push etmeyi dene
Write-Host "`nGitHub'a yükleme deneniyor..." -ForegroundColor Yellow

try {
    # Mevcut origin'i kaldır
    git remote remove origin
    Write-Host "Eski origin kaldırıldı." -ForegroundColor Green

    # Yeni origin ekle - URL'yi kendi repo URL'nizle değiştirin
    git remote add origin https://github.com/bleylek/RAG-based-BI-Platform.git
    Write-Host "Yeni origin eklendi." -ForegroundColor Green

    # Branch'i ana branch olarak ayarla ve push yap
    git branch -M master
    git push -u origin master
    Write-Host "GitHub'a push başarılı!" -ForegroundColor Green
} catch {
    Write-Host "HATA: GitHub'a push yapılamadı." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    # GitHub kimlik bilgilerini kontrol et
    Write-Host "`nGitHub kimlik bilgilerinizi kontrol edin:" -ForegroundColor Yellow
    Write-Host "1. GitHub hesabınızın bu repo için erişim yetkisi var mı?" -ForegroundColor Yellow
    Write-Host "2. Kimlik doğrulama bilgileriniz (kullanıcı adı/şifre veya token) doğru mu?" -ForegroundColor Yellow
    Write-Host "3. Repository URL'si doğru mu? URL: https://github.com/bleylek/RAG-based-BI-Platform.git" -ForegroundColor Yellow
    
    # Kişisel erişim token kullanma önerisi
    Write-Host "`nÖneri: GitHub Personal Access Token kullanın:" -ForegroundColor Cyan
    Write-Host "1. GitHub'da: Settings > Developer settings > Personal access tokens > Generate new token" -ForegroundColor White
    Write-Host "2. Token'a en azından 'repo' yetkisi verin" -ForegroundColor White
    Write-Host "3. Token'ı kopyalayın ve aşağıdaki komutu çalıştırın (token yerine kendi token'ınızı yazın):" -ForegroundColor White
    Write-Host "   git remote set-url origin https://GITHUB_USERNAME:YOUR_TOKEN@github.com/bleylek/RAG-based-BI-Platform.git" -ForegroundColor White
    Write-Host "4. Tekrar push'u deneyin: git push -u origin master" -ForegroundColor White
}

Write-Host "`nİşlem tamamlandı." -ForegroundColor Cyan
