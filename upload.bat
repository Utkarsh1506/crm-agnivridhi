@echo off
echo ===================================================
echo Uploading CRM to Hostinger via SFTP
echo ===================================================
echo.

cd /d C:\Users\Admin\Desktop\agni\CRM

echo Connecting to server...
sftp -P 65002 -b upload_to_hostinger.txt u623641178@195.35.44.250

echo.
echo Upload complete!
echo.
echo Next: SSH into server and run deployment
pause
