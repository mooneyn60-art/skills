@echo off
title Dealer Autopilot
cd /d "%~dp0"
echo %~dp0 | findstr /i "\\Temp\\ .zip" >nul && (echo. & echo It looks like this was opened from inside the ZIP file. & echo Right-click the ZIP file, choose "Extract All...", click Extract, & echo then open the new dealer-autopilot folder and double-click this file again. & echo. & pause & exit /b)
where node >nul 2>nul || (echo. & echo Node.js is not installed yet, or Windows needs a restart to find it. & echo 1. Install it from https://nodejs.org/en/download  - Windows Installer .msi, LTS & echo 2. Restart your computer, then double-click this file again. & echo. & pause & exit /b)
if not exist node_modules (echo First run: setting things up. This takes about a minute... & call npm install || (echo. & echo Setup failed. Take a photo of the messages above and send it to Claude. & pause & exit /b))
if not exist .env copy .env.example .env >nul
echo.
echo Starting Dealer Autopilot. Your browser opens in a few seconds.
echo Keep this window open while you use the app. Closing it stops the app.
echo If the browser says it cannot reach the page, wait a few seconds and refresh.
echo.
start "" cmd /c "timeout /t 5 /nobreak >nul & start http://localhost:3000"
call npm start
echo.
echo The app stopped. If you see an error above, take a photo and send it to Claude.
pause
