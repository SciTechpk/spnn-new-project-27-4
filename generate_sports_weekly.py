import feedparser
from video_rotation_engine import get_rotated_playlists
from _common import write_html_file
from datetime import datetime, timezone
import sys
import re
from urllib.parse import urlparse

# ===== 1. VERIFIED YOUTUBE PLAYLISTS (EMBED-SAFE) =====
# (Maintained as reference, actual rotation handled by video_rotation_engine.py)
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

def validate_url(url):
    """Ensure URLs are properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def parse_feeds(feed_urls):
    """Flicker-proof news feed parser with stable image handling"""
    news_items = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:  # Top 2 per feed
                # 1. Secure image handling
                img_src = None
                if hasattr(entry, 'media_content'):
                    img_src = entry.media_content[0]['url'].replace('http://', 'https://')
                elif 'description' in entry:
                    img_match = re.search(r'<img[^>]+src="([^">]+)"', entry.description)
                    if img_match:
                        img_src = img_match.group(1).replace('http://', 'https://')
                
                # 2. Stable placeholder system
                placeholder = "https://via.placeholder.com/600x400.png/eeeeee/333333?text=SPNN"
                if img_src and not validate_url(img_src):
                    img_src = None
                
                # 3. Cache-resistant output
                news_items.append({
                    "title": entry.get('title', 'No Title').strip(),
                    "link": entry.get('link', '#'),
                    "summary": (re.sub('<[^<]+?>', '', entry.get('description', 'No summary'))[:150] + '...',
                    "image": f"{img_src or placeholder}?t={datetime.now().timestamp()}"  # Cache buster
                })
        except Exception as e:
            print(f"⚠️ RSS Error ({url}): {str(e)}", file=sys.stderr)
    return news_items[:6]  # Return exactly 6 items

def generate_html():
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    
    # 1. Video Section (Stable pre-rendered HTML)
    video_boxes = get_rotated_playlists()  # From video_rotation_engine.py
    
    # 2. News Section (Flicker-proof rendering)
    news_items = parse_feeds(PRIMARY_FEEDS)
    news_boxes = ''.join(
        f'''<div class="box news-box" style="min-height:320px">
            <img src="{item['image']}" 
                 loading="eager"
                 style="height:200px;object-fit:cover;background:#f0f0f0"
                 alt="{item['title']}">
            <h3><a href="{item['link']}" target="_blank" rel="noopener">{item['title']}</a></h3>
            <p>{item['summary']}</p>
        </div>'''
        for item in news_items
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
            transform: translateY(-3px);
        }}
        .box iframe, .box img {{
            width: 100%;
            height: 200px;
            border-radius: 5px;
            border: none;
            object-fit: cover;
        }}
        .box h3 {{
            margin: 12px 0 6px;
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
            margin: 8px 0 0;
            font-size: 0.9rem;
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
            .box {{
                padding: 12px;
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
    
    <script>
        // Prevent layout shifts
        document.addEventListener('DOMContentLoaded', () => {{
            const boxes = document.querySelectorAll('.news-box');
            boxes.forEach(box => {{
                box.style.minHeight = box.offsetHeight + 'px';
            }});
        }});
    </script>
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