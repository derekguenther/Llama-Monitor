@echo off
echo ==========================================
echo       PUSH LOCAL UPDATES TO REMOTE
echo ==========================================
echo.

:: Navigate to your project folder
cd /d "C:\Users\ClaudeCode\Documents\llama-monitor"

:: Show the current status so you can see what is about to be pushed
echo --- Current Git Status ---
git status
echo --------------------------
echo.

echo If everything looks good, press any key to push your local updates to the remote repository.
echo If you are not ready, simply close this window.
pause

echo.
echo Pushing to remote...
git push origin main

echo.
echo Operation complete! 
pause