# Script to remove .env from Git tracking
# This will remove .env from Git but keep your local file

Write-Host "Removing .env from Git tracking..." -ForegroundColor Yellow

# Check if git is available
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git or add it to your PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Manual steps:" -ForegroundColor Yellow
    Write-Host "1. Open Git Bash or Command Prompt" -ForegroundColor White
    Write-Host "2. Navigate to this directory" -ForegroundColor White
    Write-Host "3. Run: git rm --cached .env" -ForegroundColor White
    Write-Host "4. Run: git commit -m 'Remove .env from version control'" -ForegroundColor White
    Write-Host "5. Run: git push origin main" -ForegroundColor White
    exit 1
}

# Check if .env is tracked
$envTracked = git ls-files .env 2>$null
if ($envTracked) {
    Write-Host ".env is currently tracked by Git" -ForegroundColor Yellow
    Write-Host "Removing from Git tracking (keeping local file)..." -ForegroundColor Yellow
    
    # Remove from Git tracking but keep local file
    git rm --cached .env
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ .env removed from Git tracking" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Commit this change: git commit -m 'Remove .env from version control'" -ForegroundColor White
        Write-Host "2. Push to GitHub: git push origin main" -ForegroundColor White
        Write-Host ""
        Write-Host "Your local .env file is safe and will remain on your computer." -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to remove .env from Git tracking" -ForegroundColor Red
    }
} else {
    Write-Host "✅ .env is NOT tracked by Git (good!)" -ForegroundColor Green
    Write-Host ""
    Write-Host "If you're still getting the error, try:" -ForegroundColor Yellow
    Write-Host "1. Make sure .env is in .gitignore (it is)" -ForegroundColor White
    Write-Host "2. Check if .env was committed in a previous commit" -ForegroundColor White
    Write-Host "3. If yes, you may need to remove it from Git history (advanced)" -ForegroundColor White
}

