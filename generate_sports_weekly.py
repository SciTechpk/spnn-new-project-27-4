import feedparser
from _common import write_html_file
from datetime import datetime, timezone
import sys
import re

# ===== 1. VIDEO THUMBNAIL LINKS (NO EMBEDS) =====
video_links = {
    "Cricket": "https://www.youtube.com/watch?v=d6R4NwdFqDI",
    "Football": "https://www.youtube.com/watch?v=Q1jq4sQYRk8",
    "Tennis": "https://www.youtube.com/watch?v=wDxX6aEYN0U",
    "Soccer": "https://www.youtube.com/watch?v=OUK2jQJ6UCw",
    "Wrestling": "https://www.youtube.com/watch?v=W9iQfgiY9xM",
    "Boxing": "https://www.youtube.com/watch?v=JjZ8V9qqm9k"
}

# ===== 2. RELIABLE RSS FEEDS =====
PRIMARY_FEEDS = [
    "https://www.espn.com/espn/rss/news",
    "https://www.bbc.com/sport/rss.xml",
    "https://www.theguardian.com/sport/rss",
    "https://sports.ndtv.com/rss/tennis",
    "https://sports.ndtv.com/rss/boxing",
    "https://www.wrestlinginc.com/feed/"
]

def generate_youtube_thumbnail(video_url):
    """Generate thumbnail URL from YouTube video URL"""
    video_id = video_url.split("v=")[1].split("&")[0]
    return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"

def parse_feeds(feed_urls):
    """Extract text news with absolute reliability"""
    news_items = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:  # Top 2 items per feed
                news_items.append({
                    "title": entry.get('title', 'No Title'),
                    "link": entry.get('link', '#'),
                    "summary": (entry.get('description', 'No summary')[:150] + '...')
                })
        except Exception as e:
            print(f"RSS Error ({url}): {str(e)}", file=sys.stderr)
    return news_items[:6]  # Return exactly 6 items

def generate_html():
    """Generate bulletproof HTML output"""
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    
    # Video boxes
    video_boxes = ''.join(
        f'''<div class="box">
            <h3>{sport}</h3>
            <a href="{url}" target="_blank">
                <img src="{generate_youtube_thumbnail(url)}" alt="{sport}">
            </a>
        </div>'''
        for sport, url in video_links.items()
    )
    
    # News boxes
    news_items = parse_feeds(PRIMARY_FEEDS)
    news_boxes = ''.join(
        f'''<div class="box">
            <h3><a href="{item['link']}" target="_blank">{item['title']}</a></h3>
            <p>{item['summary']}</p>
        </div>'''
        for item in news_items
    )
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SPNN Sports</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .box {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .box img {{
            width: 100%;
            height: 180px;
            object-fit: cover;
            border-radius: 5px;
        }}
        .box h3 {{
            margin: 10px 0 5px;
            font-size: 1.1em;
        }}
        .box a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .box a:hover {{
            text-decoration: underline;
        }}
        .box p {{
            color: #666;
            margin: 5px 0 0;
        }}
    </style>
</head>
<body>
    <h2>📺 Weekly Sports Update</h2>
    <p><em>Last updated: {timestamp}</em></p>
    
    <!-- Video Thumbnails -->
    <div class="grid">{video_boxes}</div>
    
    <!-- News Links -->
    <div class="grid">{news_boxes}</div>
</body>
</html>"""

if __name__ == "__main__":
    try:
        html_content = generate_html()
        write_html_file("news_sports_weekly.html", html_content)
        print("✅ HTML generated successfully", file=sys.stderr)
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)