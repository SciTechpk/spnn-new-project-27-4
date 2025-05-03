import feedparser
from _common import write_html_file
from datetime import datetime, timezone
import sys
import re

# ===== 1. VIDEO PLAYLISTS =====
video_playlists = {
    "Cricket": "https://www.youtube.com/embed/videoseries?list=PLl6h6UvLNv39Tguhu-5xKTz1-egoPwlZ0",
    "Boxing": "https://www.youtube.com/embed/videoseries?list=PL-KAIrL6czM_bnmP8z41QdEVCXcj0UjEA",
    "Tennis": "https://www.youtube.com/embed/videoseries?list=PLiDzi8ftbdotLBZnLcM42tHlc0D0FNEvk",
    "Football": "https://www.youtube.com/embed/videoseries?list=PLV3zWUbtkFC3mEBBsTdlQ59hiQEo_WuOT",
    "Soccer": "https://www.youtube.com/embed/videoseries?list=PLnaYFo37eXKUvS-SkkgHbMiKxFky4J7IX",
    "Wrestling": "https://www.youtube.com/embed/videoseries?list=PL51olEIebDW0IoUNpWzeBcS16XryrnpBj"
}

# ===== 2. RSS FEEDS =====
PRIMARY_FEEDS = [
    "https://www.espn.com/espn/rss/news",
    "https://www.bbc.com/sport/rss.xml",
    "https://www.theguardian.com/sport/rss",
    "https://sports.ndtv.com/rss/tennis",
    "https://sports.ndtv.com/rss/boxing",
    "https://www.wrestlinginc.com/feed/"
]

def parse_feeds(feed_urls):
    """Override _common.py's image handling"""
    news_items = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:  # Top 2 per feed
                # MANUALLY CLEAN DESCRIPTION (bypass _common.py)
                summary = re.sub('<[^<]+?>', '', entry.get('description', ''))
                summary = (summary[:150] + '...') if len(summary) > 150 else summary
                
                news_items.append({
                    "title": entry.get('title', 'No Title').strip(),
                    "link": entry.get('link', '#'),
                    "summary": summary
                })
        except Exception as e:
            print(f"⚠️ RSS Error ({url}): {str(e)}", file=sys.stderr)
    return news_items[:6]

def generate_html():
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    
    # Video Section
    video_boxes = ''.join(
        f'''<div class="box">
            <h3>{sport}</h3>
            <iframe src="{url}" frameborder="0" allowfullscreen></iframe>
        </div>'''
        for sport, url in video_playlists.items()
    )
    
    # News Section (FORCE text-only output)
    news_items = parse_feeds(PRIMARY_FEEDS)
    news_boxes = ''.join(
        f'''<div class="box news-box">
            <h3><a href="{item['link']}" target="_blank" rel="noopener">{item['title']}</a></h3>
            <p>{item['summary']}</p>
        </div>'''
        for item in news_items
    )
    
    # FINAL HTML (with image-injection protection)
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPNN Sports Weekly</title>
    <meta name="description" content="Latest sports highlights and news">
    <style>
        /* [Previous CSS unchanged] */
        .news-box img {{
            display: none !important; /* Nuclear option */
        }}
    </style>
</head>
<body>
    <h2>📺 Weekly Sports Recap</h2>
    <span class="timestamp">Last updated: {timestamp}</span>
    
    <!-- Videos -->
    <div class="grid">{video_boxes}</div>
    
    <!-- News -->
    <div class="grid">{news_boxes}</div>
    
    <!-- BLOCK _common.py IMAGE INJECTION -->
    <script>
        document.querySelectorAll('.news-box img').forEach(img => img.remove());
    </script>
</body>
</html>"""
    
    # DOUBLE-SANITIZE OUTPUT
    return re.sub(r'<img[^>]*>|loading="[^"]*"|style="[^"]*"', '', html_template)

if __name__ == "__main__":
    try:
        html_content = generate_html()
        write_html_file("news_sports_weekly.html", html_content)
        print("✅ HTML generated successfully", file=sys.stderr)
    except Exception as e:
        print(f"❌ Critical error: {str(e)}", file=sys.stderr)
        sys.exit(1)