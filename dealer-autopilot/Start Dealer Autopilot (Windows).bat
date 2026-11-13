@echo off
cd /d "%~dp0"
where node >nul 2>nul || (echo Node.js is not installed. Get the LTS version from https://nodejs.org then run this again. & pause & exit /b)
if not exist node_modules (echo First run: installing... & call npm install)
if not exist .env copy .env.example .env >nul
start "" http://localhost:3000
npm start
pause
