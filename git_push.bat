@echo off
echo ========================================================
echo Ultimate Diagram Master - GitHub Push Helper
echo ========================================================
echo.
echo This script will help you push your project to GitHub.
echo.

REM Ensure we are running from the script's directory
cd /d "%~dp0"

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed.
    echo Please install Git from https://git-scm.com/downloads
    pause
    exit /b 1
)

echo Initializing Git repository...
if not exist ".git" (
    git init
)

echo.
echo Adding files...
git add .

echo.
echo Committing changes...
git commit -m "Initial commit: Ultimate Diagram Master"

echo.
echo Please paste your GitHub Repository URL (e.g., https://github.com/username/repo.git)
set /p repo_url="URL: "

if "%repo_url%"=="" (
    echo Error: No URL provided.
    pause
    exit /b 1
)

echo.
echo Adding remote origin...
git remote remove origin >nul 2>&1
git remote add origin %repo_url%

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================================
echo Done! Your project is now on GitHub.
echo ========================================================
pause
