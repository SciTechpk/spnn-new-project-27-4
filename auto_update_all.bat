@echo off
cd /d "D:\SPNN-New-Repo-27-4-2025\spnn-new-project-27-4" || exit /b 1

:: Generate content
py generate_latest_html.py
py generate_24hr_html.py
py generate_7day_html.py
py generate_news_hourly_updated.py
py generate_psl_live.py
py generate_top5_sports.py
py generate_sports_weekly.py
py generate_youtube_iframes.py

:: Auto-push
git add --all
git commit -m "Auto-update [%date% %time%]"
git push
pause