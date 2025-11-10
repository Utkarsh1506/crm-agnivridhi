# Quick Deploy to Hostinger
# This will guide you through the upload

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Hostinger CRM Upload Guide" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Step 1: Connect to SFTP (enter password when prompted)" -ForegroundColor Yellow
Write-Host "Command: sftp -P 65002 u623641178@195.35.44.250" -ForegroundColor White
Write-Host ""
Write-Host "Step 2: Once connected, run these commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  mkdir public_html/crm.agnivridhiindia.com" -ForegroundColor Green
Write-Host "  cd public_html/crm.agnivridhiindia.com" -ForegroundColor Green
Write-Host "  lcd C:\Users\Admin\Desktop\agni\CRM" -ForegroundColor Green
Write-Host "  put manage.py" -ForegroundColor Green
Write-Host "  put requirements-production.txt" -ForegroundColor Green
Write-Host "  put passenger_wsgi.py" -ForegroundColor Green
Write-Host "  put .htaccess" -ForegroundColor Green
Write-Host "  put .env.production" -ForegroundColor Green
Write-Host "  put deploy-hostinger.sh" -ForegroundColor Green
Write-Host "  put -r accounts" -ForegroundColor Green
Write-Host "  put -r agnivridhi_crm" -ForegroundColor Green
Write-Host "  put -r applications" -ForegroundColor Green
Write-Host "  put -r bookings" -ForegroundColor Green
Write-Host "  put -r clients" -ForegroundColor Green
Write-Host "  put -r documents" -ForegroundColor Green
Write-Host "  put -r edit_requests" -ForegroundColor Green
Write-Host "  put -r notifications" -ForegroundColor Green
Write-Host "  put -r payments" -ForegroundColor Green
Write-Host "  put -r schemes" -ForegroundColor Green
Write-Host "  put -r activity_logs" -ForegroundColor Green
Write-Host "  put -r templates" -ForegroundColor Green
Write-Host "  put -r static" -ForegroundColor Green
Write-Host "  bye" -ForegroundColor Green
Write-Host ""
Write-Host "Or copy commands from: upload_commands.txt" -ForegroundColor Yellow
Write-Host ""
