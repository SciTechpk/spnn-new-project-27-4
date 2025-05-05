@echo off
:: ================== SPNN Unified Auto-Updater ==================
:: This batch file automates the generation and deployment of all SPNN pages (News, YouTube, etc.).

:: Step 1: Set working directory
cd /d D:\SPNN-New-Repo-27-4-2025\spnn-new-project-27-4 || (
    echo ❌ Failed to set working directory. Exiting...
    pause
    exit /b 1
)

:: Step 1.5: Ensure git is properly configured
call :configure_git

:: Step 2: Pull latest changes before making updates
call :git_pull_with_retry

:: Step 3: Run all Python generation scripts
call :run_python_scripts

:: Step 4: Push changes to GitHub
call :git_push_with_retry

:: Final success message
echo ✅ All updates completed successfully and pushed to GitHub.
pause
exit /b 0

::::::::::::::::::::::::::
:: FUNCTION DEFINITIONS ::
::::::::::::::::::::::::::

:configure_git
git config user.name || (
    echo ⚠ Git user.name not configured, setting default...
    git config --global user.name "SPNN Auto-Updater"
)
git config user.email || (
    echo ⚠ Git user.email not configured, setting default...
    git config --global user.email "auto-updater@spnn.example.com"
)
exit /b 0

:git_pull_with_retry
setlocal
set RETRY_COUNT=0

:pull_retry
git pull origin main && (
    echo ✓ Successfully pulled latest changes
    endlocal
    exit /b 0
)

set /a RETRY_COUNT=%RETRY_COUNT%+1
if %RETRY_COUNT% geq 3 (
    echo ❌ Failed to pull updates after 3 attempts
    endlocal
    exit /b 1
)
echo ⚠ Pull failed, retrying in 5 seconds... (Attempt %RETRY_COUNT% of 3)
timeout /t 5 /nobreak >nul
goto :pull_retry

:run_python_scripts
echo 📰 Running Python scripts for News updates...
py generate_latest_html.py || goto :python_error
py generate_24hr_html.py || goto :python_error
py generate_7day_html.py || goto :python_error
py generate_news_hourly_updated.py || goto :python_error
py generate_psl_live.py || goto :python_error
py generate_top5_sports.py || goto :python_error
py generate_sports_weekly.py || goto :python_error

echo 🎥 Running Python scripts for YouTube updates...
py generate_youtube_iframes.py || goto :python_error

exit /b 0

:python_error
echo ❌ Error running %errorlevel% python script
pause
exit /b 1

:git_push_with_retry
setlocal
set RETRY_COUNT=0

:: Stage all HTML files
git add *.html || (
    echo ❌ Failed to stage .html files
    endlocal
    exit /b 1
)

:: Create commit
git commit -m "🔄 Auto-update: Generated HTML files [%date% %time%]" || (
    echo ❌ Failed to commit changes
    endlocal
    exit /b 1
)

:push_retry
git push origin main && (
    echo ✓ Successfully pushed changes
    endlocal
    exit /b 0
)

set /a RETRY_COUNT=%RETRY_COUNT%+1
if %RETRY_COUNT% geq 3 (
    echo ❌ Failed to push updates after 3 attempts
    endlocal
    exit /b 1
)
echo ⚠ Push failed, retrying in 10 seconds... (Attempt %RETRY_COUNT% of 3)
timeout /t 10 /nobreak >nul
goto :push_retry