@echo off
cd /d "c:\Users\Admin\Desktop\agni\CRM"

echo ========================================
echo Adding all changes to git...
echo ========================================
git add .

echo.
echo ========================================
echo Committing changes...
echo ========================================
git commit -m "Add complete agreements system with PDF generation, templates, and documentation"

echo.
echo ========================================
echo Pushing to remote repository...
echo ========================================
git push

echo.
echo ========================================
echo GIT PUSH COMPLETE!
echo ========================================
pause
