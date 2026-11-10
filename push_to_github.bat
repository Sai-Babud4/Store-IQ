@echo off
setlocal
echo ========================================================
echo   RetailIQ - One-Click Push to GitHub (RetailIQ2)
echo ========================================================
echo.

cd /d "%~dp0"

set DEFAULT_URL=https://github.com/Sai-Babud4/RetailIQ2.git
set /p REPO_URL="Press Enter to use [%DEFAULT_URL%] or paste a custom URL: "
if "%REPO_URL%"=="" set REPO_URL=%DEFAULT_URL%

echo.
echo Using repository: %REPO_URL%
echo.

echo [1/3] Configuring remote origin...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [2/3] Staging all files and folders (including src/, api/, data/)...
git add .
git commit -m "RetailIQ: Complete fullstack deployment with src, api, and database" 2>nul

echo [3/3] Pushing to GitHub main branch...
git branch -M main
git push -u -f origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   SUCCESS! All folders (src, api, data) pushed to GitHub!
    echo   Vercel will now automatically build and deploy!
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo   [NOTE] If GitHub prompted for credentials, please sign in.
    echo ========================================================
)
pause
