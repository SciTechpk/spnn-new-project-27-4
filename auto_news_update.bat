@echo off
:: ====== SPNN GitHub Auto-Updater Batch ======
:: Set working directory where your scripts and HTML files are stored
cd /d D:\SPNN-Backup\spnn-news-auto\spnn-news-auto

:: Activate Python script execution (each script updates a page)
echo Running Python scripts...
py generate_latest_html.py
py generate_24hr_html.py
py generate_7day_html.py
py generate_psl_live.py
py generate_top5_sports.py
py generate_sports_weekly.py

:: Optional future additions (ticker, YouTube) can go here
:: py generate_ticker.py
:: py generate_youtube_clips.py


:: Push updates to GitHub
echo Updating GitHub repo...
git add *.html
git commit -m "🔁 Auto update HTML files from local machine"
git push origin main

echo ✅ News updated and pushed to GitHub successfully.
pause
