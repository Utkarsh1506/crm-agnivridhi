# Automated SFTP Upload Script for Hostinger
# Run this from PowerShell in your project directory

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Uploading Agnivridhi CRM to crm.agnivridhiindia.com" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$sourceDir = "C:\Users\Admin\Desktop\agni\CRM"
$sftpHost = "195.35.44.250"
$sftpPort = "65002"
$sftpUser = "u623641178"
$remotePath = "/home/u623641178/public_html/crm.agnivridhiindia.com"

Write-Host "Connecting via SFTP to $sftpHost..." -ForegroundColor Yellow

# Use sftp batch mode with the upload script
sftp -P $sftpPort -b upload_to_hostinger.txt "$sftpUser@$sftpHost"

Write-Host ""
Write-Host "Upload complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Connect via SSH: ssh -p $sftpPort $sftpUser@$sftpHost" -ForegroundColor White
Write-Host "2. Navigate: cd ~/public_html/crm.agnivridhiindia.com" -ForegroundColor White
Write-Host "3. Rename env: mv .env.production .env" -ForegroundColor White
Write-Host "4. Run deploy: chmod +x deploy-hostinger.sh && ./deploy-hostinger.sh" -ForegroundColor White
Write-Host ""
