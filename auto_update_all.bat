@echo off
:: ================== SPNN Unified Auto-Updater ==================
:: This batch file automates the generation and deployment of all SPNN pages (News, YouTube, etc.).

:: Step 1: Set working directory
cd /d D:\SPNN-New-Repo-27-4-2025\spnn-new-project-27-4 || (
    echo ❌ Failed to set working directory. Exiting...
    pause
    exit /b 1
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
    echo ❌ Error running generate_7day_html.py
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
git commit -m "🔄 Auto-update: Generated HTML files for News, YouTube, and other content" || (
    echo ❌ Failed to commit changes
    pause
    exit /b 1
)

:: Push changes to GitHub
git push origin main || (
    echo ❌ Failed to push updates to GitHub
    pause
    exit /b 1
)

:: Step 5: Notify completion
echo ✅ All updates completed successfully and pushed to GitHub.
pause