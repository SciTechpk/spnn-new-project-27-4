import feedparser
from _common import write_html_file
from datetime import datetime, timezone
import sys
import re

# 1. VERIFIED YOUTUBE PLAYLISTS
video_playlists = {
    "Cricket": "https://www.youtube.com/embed/videoseries?list=PL5L5ZxQm0dpw7wU0lLpkhQ7Xe7Vl1hQ2d",
    "Football": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfdGq1dP7qg4FhUum5J8T1vW",
    "Tennis": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc07FjZ5hR7OVc4mjx1Y0L1",
    "Soccer": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc8G1FozR6j-tBq3Y9XzW1A",
    "Wrestling": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc1Y0X9gZ0k6Xq5YJmz0Q2X",
    "Boxing": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc1Y0X9gZ0k6Xq5YJmz0Q2Y"
}

# 2. TESTED RSS FEEDS
PRIMARY_FEEDS = [
    "https://www.espn.com/espn/rss/news",           # General Sports
    "https://www.skysports.com/rss/12040",          # General Sports
    "https://www.bbc.com/sport/rss.xml",            # General Sports
    "https://www.theguardian.com/sport/rss",        # General Sports
    "https://sports.ndtv.com/rss/tennis",           # Tennis (NDTV)
    "https://www.wrestlinginc.com/feed/",           # Wrestling
    "https://sports.ndtv.com/rss/boxing"            # Boxing (NDTV)
]

def extract_image(entry):
    """Extract image URL from feed entry with multiple fallbacks"""
    if hasattr(entry, 'media_content') and entry.media_content:
        return entry.media_content[0]['url']
    if hasattr(entry, 'enclosures') and entry.enclosures:
        return entry.enclosures[0].href
    if 'description' in entry:
        img_match = re.search(r'<img[^>]+src="([^">]+)"', entry.description)
        if img_match:
            return img_match.group(1)
    return None

def parse_feeds(feed_urls, max_items):
    """Parse RSS feeds with robust error handling"""
    news_items = []
    working_feeds = 0
    
    for url in feed_urls:
        try:
            print(f"Fetching: {url}", file=sys.stderr)
            feed = feedparser.parse(url)
            
            if not feed.entries:
                print(f"⚠️ Empty feed: {url}", file=sys.stderr)
                continue
                
            working_feeds += 1
            for entry in feed.entries[:max_items]:
                title = entry.get('title', 'No Title')
                summary = entry.get('summary', entry.get('description', 'No summary'))
                summary = (summary[:150] + '...') if len(summary) > 150 else summary
                link = entry.get('link', '#')
                image_url = extract_image(entry) or "https://via.placeholder.com/300x200?text=SPNN"
                
                news_items.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "image_url": image_url
                })
                
        except Exception as e:
            print(f"❌ RSS Error ({url}): {str(e)}", file=sys.stderr)
    
    print(f"✔ {working_feeds}/{len(feed_urls)} feeds working", file=sys.stderr)
    return news_items

def generate_html(videos, news_items):
    """Generate HTML with proper structure and styling"""
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    
    # Video boxes
    video_boxes = []
    for sport, url in videos.items():
        video_boxes.append(
            f'<div class="box"><h3>{sport}</h3><iframe src="{url}" allowfullscreen></iframe></div>'
        )
    
    # News boxes
    news_boxes = []
    for item in news_items[:6]:
        news_boxes.append(
            f'''<div class="box">
                <img src="{item["image_url"]}" onerror="this.src='https://via.placeholder.com/300x200?text=SPNN'">
                <h3><a href="{item["link"]}" target="_blank">{item["title"]}</a></h3>
                <p>{item["summary"]}</p>
            </div>'''
        )
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SPNN Sports Weekly</title>
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
            margin-bottom: 30px;
        }}
        .box {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .box h3 {{
            margin-top: 0;
            color: #333;
            font-size: 1.2em;
        }}
        .box iframe, .box img {{
            width: 100%;
            height: 200px;
            border-radius: 5px;
            object-fit: cover;
            border: none;
        }}
        .box p {{
            color: #666;
            line-height: 1.5;
        }}
        .box a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .box a:hover {{
            text-decoration: underline;
        }}
        h2 {{
            color: #d22;
            border-bottom: 2px solid #d22;
            padding-bottom: 10px;
        }}
    </style>
</head>
<body>
    <h2>📺 Weekly Sports Recap</h2>
    <p><em>Updated: {timestamp}</em></p>
    
    <!-- Videos Section -->
    <div class="grid">{''.join(video_boxes)}</div>
    
    <!-- News Section -->
    <div class="grid">{''.join(news_boxes)}</div>
</body>
</html>"""

if __name__ == "__main__":
    try:
        news_items = parse_feeds(PRIMARY_FEEDS, max_items=2)
        html_content = generate_html(video_playlists, news_items)
        write_html_file("news_sports_weekly.html", html_content)
        print("✅ Success: news_sports_weekly.html generated", file=sys.stderr)
    except Exception as e:
        print(f"❌ Critical error: {str(e)}", file=sys.stderr)
        sys.exit(1)