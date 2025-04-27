import requests
from datetime import datetime

API_KEY = "AIzaSyADRyWjUl0xfBVCkW8r-3YoM_72e5Qso2c"

# ✅ Your confirmed playlists
playlists = {
    "news_psl_live.html": "PLrr-WIVYH-Xi8P1a_8fOq5949f-Gwndo_",  # 1 PSL live highlight
    "news_top5_sports.html": "PLrr-WIVYH-XhKGfRbjeddC8S9QwkVazMH",  # 5 Top moments
    "news_sports_weekly.html": {
        "Cricket": "PLH06VbPakyYUnpMhUFZLp6pbGfYTDf3-S",
        "Football": "PLzn2Kbs0lFDsKiN04bQ2AsobsvV2U7S36",
        "Tennis": "PLQHHr8gPOsH6KEvZs8n8-l4UXJuLz9GJn"
    }
}

def fetch_video_iframes(playlist_id, max_results):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}"
    response = requests.get(url).json()
    items = response.get("items", [])
    iframes = []
    for item in items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        iframe = f'<iframe width="100%" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
        iframes.append(iframe)
    return iframes

def generate_page(filename, title, iframe_blocks):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>SPNN - YouTube Videos</title></head>
<body>
<h2>📺 {title}</h2>
<p><em>Updated: {timestamp}</em></p>
{''.join(iframe_blocks)}
</body>
</html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

# ✅ Generate PSL Live page (1 long video)
generate_page(
    "news_psl_live.html",
    "PSL 2025 – Live Coverage",
    fetch_video_iframes(playlists["news_psl_live.html"], 1)
)

# ✅ Generate Top 5 Moments (5 short clips)
generate_page(
    "news_top5_sports.html",
    "Top 5 Moments – PSL 2025",
    fetch_video_iframes(playlists["news_top5_sports.html"], 5)
)

# ✅ Generate Weekly Sports Recap (1 each from 3 sports)
weekly_iframes = []
for sport, playlist_id in playlists["news_sports_weekly.html"].items():
    weekly_iframes.append(f"<h3>{sport} Highlights</h3>")
    weekly_iframes += fetch_video_iframes(playlist_id, 1)

generate_page(
    "news_sports_weekly.html",
    "Weekly Sports Recap",
    weekly_iframes
)
