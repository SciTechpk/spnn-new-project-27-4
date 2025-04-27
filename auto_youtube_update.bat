@echo off
:: === SPNN YouTube Auto-Updater ===
cd /d D:\SPNN-Backup\spnn-news-auto\spnn-news-auto

:: Run YouTube iframe generator only
py generate_youtube_iframes.py

:: Push updated iframe HTML files to GitHub
git add *.html
git commit -m "🎥 Auto update YouTube iframe content"
git push origin main

echo ✅ YouTube iframe update complete.
pause
