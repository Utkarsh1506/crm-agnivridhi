@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo Uploading Agnivridhi CRM to Hostinger
echo ====================================================
echo.

cd /d C:\Users\Admin\Desktop\agni\CRM

echo Creating SFTP batch file with credentials...
(
echo open u623641178@195.35.44.250:65002
echo agnivridhi@CRM121
echo mkdir public_html/crm.agnivridhiindia.com
echo cd public_html/crm.agnivridhiindia.com
echo lcd C:\Users\Admin\Desktop\agni\CRM
echo put manage.py
echo put requirements-production.txt
echo put passenger_wsgi.py
echo put .htaccess
echo put .env.production
echo put deploy-hostinger.sh
echo put export_sqlite_data.py
echo put import_to_mysql.py
echo put -r accounts
echo put -r agnivridhi_crm
echo put -r applications
echo put -r bookings
echo put -r clients
echo put -r documents
echo put -r edit_requests
echo put -r notifications
echo put -r payments
echo put -r schemes
echo put -r activity_logs
echo put -r templates
echo put -r static
echo bye
) > sftp_upload_batch.txt

echo Connecting and uploading...
echo.

psftp -batch -b sftp_upload_batch.txt

if errorlevel 1 (
    echo.
    echo Upload failed! Trying alternative method with sftp...
    echo.
    sftp -P 65002 -b upload_to_hostinger.txt u623641178@195.35.44.250
)

echo.
echo ====================================================
echo Upload Complete!
echo ====================================================
echo.
echo Next: Connect via SSH and deploy
echo ssh -p 65002 u623641178@195.35.44.250
echo.
pause
