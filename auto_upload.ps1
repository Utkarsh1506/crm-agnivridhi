$password = "agnivridhi@CRM121"
$username = "u623641178"
$serverHost = "195.35.44.250"
$port = "65002"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Uploading Agnivridhi CRM to Hostinger" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Create expect-like script for password automation
$batchCommands = @"
mkdir public_html/crm.agnivridhiindia.com
cd public_html/crm.agnivridhiindia.com
lcd C:\Users\Admin\Desktop\agni\CRM
put manage.py
put requirements-production.txt
put passenger_wsgi.py
put .htaccess
put .env.production
put deploy-hostinger.sh
put export_sqlite_data.py
put import_to_mysql.py
put -r accounts
put -r agnivridhi_crm
put -r applications
put -r bookings
put -r clients
put -r documents
put -r edit_requests
put -r notifications
put -r payments
put -r schemes
put -r activity_logs
put -r templates
put -r static
bye
"@

$batchCommands | Out-File -FilePath "sftp_batch.txt" -Encoding ASCII

Write-Host "Connecting to $serverHost..." -ForegroundColor Yellow
Write-Host "You may need to enter password: $password" -ForegroundColor Yellow
Write-Host ""

# Use sshpass alternative or expect
$env:SSHPASS = $password

# Try using sftp
& sftp -P $port -b sftp_batch.txt "$username@$serverHost"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=====================================================" -ForegroundColor Green
    Write-Host "Upload Successful!" -ForegroundColor Green
    Write-Host "=====================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "1. SSH into server: ssh -p $port $username@$serverHost" -ForegroundColor White
    Write-Host "2. Password: $password" -ForegroundColor White
    Write-Host "3. Deploy: cd ~/public_html/crm.agnivridhiindia.com && chmod +x deploy-hostinger.sh && ./deploy-hostinger.sh" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "=====================================================" -ForegroundColor Red
    Write-Host "Upload Failed - Manual SFTP Required" -ForegroundColor Red
    Write-Host "=====================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Run this command manually:" -ForegroundColor Yellow
    Write-Host "sftp -P $port $username@$serverHost" -ForegroundColor White
    Write-Host "Password: $password" -ForegroundColor White
    Write-Host "Then paste commands from: sftp_batch.txt" -ForegroundColor White
}
