@echo off
setlocal EnableExtensions
cd /d "E:\smart campus one"

title SmartCampus One - GitHub Auto Update
color 0B

echo.
echo ========================================================
echo          SMARTCAMPUS ONE - GITHUB AUTO UPDATE
echo ========================================================
echo.

where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not available in PATH.
    echo Install Git for Windows, then run this file again.
    pause
    exit /b 1
)

if not exist ".git" (
    echo [FIRST RUN] Setting up this folder as the Git repository...
    git init
    if errorlevel 1 goto :error

    git branch -M main
    git remote add origin https://github.com/abhishek027aks/smartcampus-one.git 2>nul

    echo.
    echo [FIRST RUN] Uploading your local SmartCampus One files to GitHub...
    echo NOTE: The existing initial GitHub commit may be replaced so your
    echo local professional README/files become the repository source.
    echo.

    git add .
    if errorlevel 1 goto :error

    git commit -m "feat: initialize SmartCampus One project"
    if errorlevel 1 (
        echo [INFO] Nothing new to commit, continuing...
    )

    git push -u origin main --force
    if errorlevel 1 goto :pusherror

    echo.
    echo ========================================================
    echo   FIRST SETUP COMPLETE - GITHUB UPDATED SUCCESSFULLY
    echo ========================================================
    echo.
    echo From now on, just double-click this same file.
    echo It will automatically add, commit and push your changes.
    echo.
    pause
    exit /b 0
)

REM ----------------------------------------------------------
REM Normal one-click update
REM ----------------------------------------------------------

echo [1/4] Checking GitHub connection...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [ERROR] GitHub remote is missing.
    echo Adding: https://github.com/abhishek027aks/smartcampus-one.git
    git remote add origin https://github.com/abhishek027aks/smartcampus-one.git
    if errorlevel 1 goto :error
)

echo [2/4] Checking local changes...
git status --short

git add -A
if errorlevel 1 goto :error

REM Create a commit only when there are changes.
git diff --cached --quiet
if errorlevel 1 (
    for /f "tokens=1-3 delims=/ " %%a in ("%date%") do set D=%%c-%%a-%%b
    for /f "tokens=1-2 delims=:" %%a in ("%time%") do set T=%%a:%%b
    git commit -m "update: SmartCampus One project"
    if errorlevel 1 goto :error
) else (
    echo [INFO] No local changes found.
)

echo [3/4] Syncing with GitHub...
git pull --rebase origin main
if errorlevel 1 (
    echo.
    echo [WARNING] GitHub has changes that could not be rebased automatically.
    echo Resolve the conflict manually, then run this file again.
    pause
    exit /b 1
)

echo [4/4] Pushing to GitHub...
git push origin main
if errorlevel 1 goto :pusherror

echo.
echo ========================================================
echo        SUCCESS - GITHUB IS UP TO DATE
echo ========================================================
echo.
echo Repository: https://github.com/abhishek027aks/smartcampus-one
echo.
pause
exit /b 0

:error
echo.
echo ========================================================
echo                 UPDATE FAILED
echo ========================================================
echo Check the message above and try again.
pause
exit /b 1

:pusherror
echo.
echo ========================================================
echo                 PUSH FAILED
echo ========================================================
echo.
echo Most common reason: GitHub authentication is not set up.
echo Sign in through Git Credential Manager / GitHub CLI, then run again.
echo.
pause
exit /b 1
