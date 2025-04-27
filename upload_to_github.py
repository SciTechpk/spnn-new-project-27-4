# ✅ upload_to_github.py — Push all HTML files to GitHub Pages

import os
import subprocess
from datetime import datetime

html_files = [
    "news_latest.html",
    "news_24hr.html",
    "news_7day.html",
    "news_psl_live.html",
    "news_psl_top5.html",
    "news_top5_sports.html",     # ✅ Newly added
    "news_sports_weekly.html"    # ✅ Newly added
]

timestamp = datetime.utcnow().strftime("📡 Auto-update: %Y-%m-%d %H:%M:%S")

for file in html_files:
    with open(file, "r+", encoding="utf-8") as f:
        content = f.read()
        f.seek(0)
        f.write(f"<!-- {timestamp} -->\n{content}")
        f.truncate()

subprocess.run(["git", "add"] + html_files)
subprocess.run(["git", "commit", "-m", f"{timestamp}"])
subprocess.run(["git", "push"])
