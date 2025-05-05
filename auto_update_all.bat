@echo off
:: ================== SPNN Unified Auto-Updater ==================
:: This batch file automates the generation and deployment of all SPNN pages (News, YouTube, etc.).

:: Step 1: Set working directory
cd /d D:\SPNN-New-Repo-27-4-2025\spnn-new-project-27-4 || (
    echo ❌ Failed to set working directory. Exiting...
    pause
    exit /b 1
)

:: Step 1.5: Ensure git is configured
git config user.name || (
    echo ⚠ Git user.name not configured, setting default...
    git config --global user.name "SPNN Auto-Updater"
)
git config user.email || (
    echo ⚠ Git user.email not configured, setting default...
    git config --global user.email "auto-updater@spnn.example.com"
)

:: Step 2: Run Python scripts for News updates
echo 📰 Running Python scripts for News updates...
py generate_latest_html.py || (
    echo ❌ Error running generate_latest_html.py
    pause
    exit /b 1
)
py generate_24hr_html.py || (
    echo ❌ Error running generate_24hr_html.py
    pause
    exit /b 1
)
py generate_7day_html.py || (
    echo ❌ Error running generate_7day_html.py
    pause
    exit /b 1
)
py generate_news_hourly_updated.py || (
    echo ❌ Error running generate_news_hourly_updated.py
    pause
    exit /b 1
)
py generate_psl_live.py || (
    echo ❌ Error running generate_psl_live.py
    pause
    exit /b 1
)
py generate_top5_sports.py || (
    echo ❌ Error running generate_top5_sports.py
    pause
    exit /b 1
)
py generate_sports_weekly.py || (
    echo ❌ Error running generate_sports_weekly.py
    pause
    exit /b 1
)

:: Step 3: Run Python scripts for YouTube updates
echo 🎥 Running Python scripts for YouTube updates...
py generate_youtube_iframes.py || (
    echo ❌ Error running generate_youtube_iframes.py
    pause
    exit /b 1
)

:: Step 4: Push updated HTML files to GitHub
echo 🔧 Committing and pushing updates to GitHub...

:: Add all .html files in the root directory
git add *.html || (
    echo ❌ Failed to stage .html files
    pause
    exit /b 1
)

:: Commit with a more descriptive message
git commit -m "🔄 Auto-update: Generated HTML files for News, YouTube, and other content [%date% %time%]" || (
    echo ❌ Failed to commit changes
    pause
    exit /b 1
)

:: Push changes to GitHub with retry logic
set RETRY_COUNT=0
:push_retry
git push origin main && goto :push_success

set /a RETRY_COUNT=%RETRY_COUNT%+1
if %RETRY_COUNT% geq 3 (
    echo ❌ Failed to push updates to GitHub after 3 attempts
    pause
    exit /b 1
)
echo ⚠ Push failed, retrying in 5 seconds... (Attempt %RETRY_COUNT% of 3)
timeout /t 5 /nobreak >nul
goto :push_retry

:push_success
:: Step 5: Notify completion
echo ✅ All updates completed successfully and pushed to GitHub.
pause