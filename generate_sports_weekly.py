import feedparser
from video_rotation_engine import get_rotated_playlists
from _common import write_html_file
from datetime import datetime, timezone
import sys
import re
from urllib.parse import urlparse

# ===== 1. PRE-DESIGNED SVG PLACEHOLDERS =====
SVG_TEMPLATES = [
    # Trophy (Gold/Blue)
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200"><rect width="100%" height="100%" fill="#1e3c72"/><path d="M150 40L120 80H80V60H40V120H80V100L150 160L220 100V120H260V60H220V80H180L150 40Z" fill="#f5d76e"/><text x="50%" y="85%" fill="white" font-family="Arial" text-anchor="middle" font-size="14">SPNN Sports</text></svg>''',
    
    # Soccer (Green/White)
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200"><rect width="100%" height="100%" fill="#27ae60"/><circle cx="150" cy="100" r="50" fill="#2c3e50"/><path d="M150 50L150 150M100 100H200" stroke="#ecf0f1" stroke-width="8"/></svg>''',
    
    # Boxing (Red/Orange)
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200"><rect width="100%" height="100%" fill="#e74c3c"/><path d="M100 80L120 60L180 120L160 140Z" fill="#f39c12"/></svg>''',
    
    # Racing (Blue/Yellow)
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200"><rect width="100%" height="100%" fill="#3498db"/><path d="M50 150L250 150M200 120L250 150L200 180" stroke="#f1c40f" stroke-width="10"/></svg>'''
]

# ===== 2. VIDEO PLAYISTS (UNCHANGED) =====
video_playlists = {
    "Cricket": "https://www.youtube.com/embed/videoseries?list=PLl6h6UvLNv39Tguhu-5xKTz1-egoPwlZ0",
    "Boxing": "https://www.youtube.com/embed/videoseries?list=PL-KAIrL6czM_bnmP8z41QdEVCXcj0UjEA",
    "Tennis": "https://www.youtube.com/embed/videoseries?list=PLiDzi8ftbdotLBZnLcM42tHlc0D0FNEvk",
    "Football": "https://www.youtube.com/embed/videoseries?list=PLV3zWUbtkFC3mEBBsTdlQ59hiQEo_WuOT",
    "Soccer": "https://www.youtube.com/embed/videoseries?list=PLnaYFo37eXKUvS-SkkgHbMiKxFky4J7IX",
    "Wrestling": "https://www.youtube.com/embed/videoseries?list=PL51olEIebDW0IoUNpWzeBcS16XryrnpBj"
}

# ===== 3. RSS FEEDS (UNCHANGED) =====
PRIMARY_FEEDS = [
    "https://www.espn.com/espn/rss/news",
    "https://www.bbc.com/sport/rss.xml",
    "https://www.theguardian.com/sport/rss",
    "https://sports.ndtv.com/rss/tennis",
    "https://sports.ndtv.com/rss/boxing",
    "https://www.wrestlinginc.com/feed/"
]

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def parse_feeds(feed_urls):
    """Process feeds with top 2 keeping images, rest using SVGs"""
    news_items = []
    svg_index = 0  # Track which SVG to use
    
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry_idx, entry in enumerate(feed.entries[:2]):  # Top 2 per feed
                # First 2 items keep original images
                if len(news_items) < 2:
                    img_src = None
                    if hasattr(entry, 'media_content'):
                        img_src = entry.media_content[0]['url'].replace('http://', 'https://')
                    elif 'description' in entry:
                        img_match = re.search(r'<img[^>]+src="([^">]+)"', entry.description)
                        if img_match:
                            img_src = img_match.group(1).replace('http://', 'https://')
                    
                    if not img_src or not validate_url(img_src):
                        img_src = "data:image/svg+xml;utf8," + SVG_TEMPLATES[svg_index % 4]
                        svg_index += 1
                # Items 3-6 use SVGs only
                else:
                    img_src = "data:image/svg+xml;utf8," + SVG_TEMPLATES[svg_index % 4]
                    svg_index += 1
                
                news_items.append({
                    "title": entry.get('title', 'No Title').strip(),
                    "link": entry.get('link', '#'),
                    "summary": (re.sub('<[^<]+?>', '', entry.get('description', 'No summary'))[:150] + '...',
                    "image": img_src,
                    "is_svg": len(news_items) >= 2  # Flag for SVG items
                })
        except Exception as e:
            print(f"⚠️ RSS Error ({url}): {str(e)}", file=sys.stderr)
    return news_items[:6]  # Exactly 6 items

def generate_html():
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    
    # Video Section (Unchanged)
    video_boxes = get_rotated_playlists()
    
    # News Section (Modified for SVG support)
    news_items = parse_feeds(PRIMARY_FEEDS)
    news_boxes = ''.join(
        f'''<div class="box news-box" {'data-has-svg="true"' if item['is_svg'] else ''}>
            <img src="{item['image']}" 
                 loading="eager"
                 style="{'width:80%;height:auto' if item['is_svg'] else 'height:200px;object-fit:cover'}"
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
            border-radius: 5px;
            border: none;
            object-fit: cover;
        }}
        .box[data-has-svg] {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }}
        .box[data-has-svg] img {{
            width: 80% !important;
            height: auto !important;
            margin-bottom: 10px;
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
        // Stability lock for news boxes
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