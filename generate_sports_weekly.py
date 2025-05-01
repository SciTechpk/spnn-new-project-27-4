import feedparser
from video_rotation_engine import get_rotated_playlists
from _common import write_html_file
from datetime import datetime, timezone
import sys
import re

# ===== 1. VERIFIED YOUTUBE PLAYLISTS (EMBED-SAFE) =====
# (Kept as fallback reference, not used directly)
video_playlists = {
    "Cricket": "https://www.youtube.com/embed/videoseries?list=PLl6h6UvLNv39Tguhu-5xKTz1-egoPwlZ0",
    "Boxing": "https://www.youtube.com/embed/videoseries?list=PL-KAIrL6czM_bnmP8z41QdEVCXcj0UjEA",
    "Tennis": "https://www.youtube.com/embed/videoseries?list=PLiDzi8ftbdotLBZnLcM42tHlc0D0FNEvk",
    "Football": "https://www.youtube.com/embed/videoseries?list=PLV3zWUbtkFC3mEBBsTdlQ59hiQEo_WuOT",
    "Soccer": "https://www.youtube.com/embed/videoseries?list=PLnaYFo37eXKUvS-SkkgHbMiKxFky4J7IX",
    "Wrestling": "https://www.youtube.com/embed/videoseries?list=PL51olEIebDW0IoUNpWzeBcS16XryrnpBj"
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

def generate_playlist_thumbnail(playlist_url):
    """Generate playlist thumbnail using first video in playlist"""
    try:
        video_id = playlist_url.split("list=")[1].split("&")[0]
        return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
    except (IndexError, AttributeError):
        return "https://via.placeholder.com/300x200?text=SPNN"

def parse_feeds(feed_urls):
    """Extract news with image fallback"""
    news_items = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:  # Top 2 per feed
                img_src = None
                if hasattr(entry, 'media_content'):
                    img_src = entry.media_content[0]['url']
                elif 'description' in entry:
                    img_match = re.search(r'<img[^>]+src="([^">]+)"', entry.description)
                    if img_match:
                        img_src = img_match.group(1)
                
                news_items.append({
                    "title": entry.get('title', 'No Title').strip(),
                    "link": entry.get('link', '#'),
                    "summary": (entry.get('description', 'No summary')[:150] + '...'),
                    "image": img_src or "https://via.placeholder.com/300x200?text=SPNN"
                })
        except Exception as e:
            print(f"⚠️ RSS Error ({url}): {str(e)}", file=sys.stderr)
    return news_items[:6]

def generate_html():
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    
    # Video Section (Fixed rotation implementation)
    video_boxes = ''.join(
        f'''<div class="box">
            <h3>{sport}</h3>
            <iframe src="{url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>'''
        for sport, url in get_rotated_playlists().items()  # Removed duplicate .items()
    )
    
    # News Section
    news_boxes = ''.join(
        f'''<div class="box">
            <img src="{item['image']}" alt="{item['title']}" loading="lazy" onerror="this.src='https://via.placeholder.com/300x200?text=SPNN'">
            <h3><a href="{item['link']}" target="_blank" rel="noopener noreferrer">{item['title']}</a></h3>
            <p>{item['summary']}</p>
        </div>'''
        for item in parse_feeds(PRIMARY_FEEDS)
    )
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPNN Sports Weekly</title>
    <meta name="description" content="Latest sports highlights and news">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
            line-height: 1.6;
        }}
        h2 {{
            color: #d22;
            border-bottom: 2px solid #d22;
            padding-bottom: 10px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .box {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .box:hover {{
            transform: translateY(-5px);
        }}
        .box iframe, .box img {{
            width: 100%;
            height: 200px;
            border-radius: 5px;
            border: none;
            object-fit: cover;
        }}
        .box h3 {{
            margin: 10px 0 5px;
            font-size: 1.1rem;
        }}
        .box a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .box a:hover {{
            text-decoration: underline;
        }}
        .box p {{
            color: #555;
            margin: 5px 0 0;
        }}
        .timestamp {{
            color: #666;
            font-style: italic;
            margin-bottom: 20px;
            display: block;
        }}
        @media (max-width: 600px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
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
</body>
</html>"""

if __name__ == "__main__":
    try:
        html_content = generate_html()
        write_html_file("news_sports_weekly.html", html_content)
        print("✅ HTML generated successfully", file=sys.stderr)
    except Exception as e:
        print(f"❌ Critical error: {str(e)}", file=sys.stderr)
        sys.exit(1)