@echo off
:: ================== SPNN Ultimate Auto-Push Solution ==================

:: 1. Set working directory
cd /d "D:\SPNN-New-Repo-27-4-2025\spnn-new-project-27-4" || (
    echo ❌ Failed to set working directory
    pause
    exit /b 1
)

:: 2. Generate all content
echo 📊 Generating all content...
py generate_latest_html.py && \
py generate_24hr_html.py && \
py generate_7day_html.py && \
py generate_news_hourly_updated.py && \
py generate_psl_live.py && \
py generate_top5_sports.py && \
py generate_sports_weekly.py && \
py generate_youtube_iframes.py || (
    echo ❌ Error in content generation
    pause
    exit /b 1
)

:: 3. Git operations
echo 💻 Preparing GitHub commit...
git add --all && \
git commit -m "🔄 Auto-update: All content [%date% %time%]" && \
git push origin main || (
    echo ❌ Git operations failed
    echo ℹ Attempting GitHub Desktop fallback...
    call :trigger_ghdt
)

:: 4. Final verification
git status | find "Your branch is up to date" >nul && (
    echo ✅ Successfully pushed all changes!
    goto :end
)

:ghdt_push_needed
echo ℹ Please click [Push origin] in GitHub Desktop
start "" "C:\Users\%USERNAME%\AppData\Local\GitHubDesktop\GitHubDesktop.exe" --focus
goto :end

:trigger_ghdt
start "" "C:\Users\%USERNAME%\AppData\Local\GitHubDesktop\app-*\resources\app\static\github.bat" push --repo "D:\SPNN-New-Repo-27-4-2025\spnn-new-project-27-4"
timeout /t 5 /nobreak >nul
goto :ghdt_push_needed

:end
pause