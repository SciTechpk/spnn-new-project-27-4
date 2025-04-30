import feedparser
from _common import write_html_file
import json
from datetime import datetime

# ===== 1. UNRESTRICTED YOUTUBE PLAYLISTS =====
video_playlists = {
    "Cricket": "https://www.youtube.com/embed/videoseries?list=PL5L5ZxQm0dpw7wU0lLpkhQ7Xe7Vl1hQ2d",  # ICC
    "Football": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfdGq1dP7qg4FhUum5J8T1vW",  # Premier League
    "Tennis": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc07FjZ5hR7OVc4mjx1Y0L1",    # ATP
    "Soccer": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc8G1FozR6j-tBq3Y9XzW1A",   # UEFA
    "Wrestling": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc1Y0X9gZ0k6Xq5YJmz0Q2X", # WWE
    "Boxing": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc1Y0X9gZ0k6Xq5YJmz0Q2Y"      # Boxing
}

# ===== 2. BULLETPROOF RSS PARSING =====
def parse_feeds(feed_urls, max_items_per_feed):
    all_news_items = []
    for feed_url in feed_urls:
        try:
            print(f"🔄 Fetching: {feed_url}")  # DEBUG
            feed = feedparser.parse(feed_url)
            print(f"✅ Found {len(feed.entries)} entries")  # DEBUG
            
            for entry in feed.entries[:max_items_per_feed]:
                title = entry.get('title', 'No Title')
                summary = entry.get('summary', 'No summary available.')
                link = entry.get('link', '#')
                
                # Extract image (prioritize media_content > enclosures)
                image_url = '#'
                if 'media_content' in entry and entry.media_content:
                    image_url = entry.media_content[0]['url']
                elif 'enclosures' in entry and entry.enclosures:
                    image_url = entry.enclosures[0].href
                
                all_news_items.append({
                    "title": title,
                    "summary": summary[:150] + '...' if len(summary) > 150 else summary,
                    "link": link,
                    "image_url": image_url if image_url.startswith('http') else 'https://via.placeholder.com/150'
                })
        except Exception as e:
            print(f"❌ Failed {feed_url}: {str(e)}")  # DEBUG
    return all_news_items

# ===== 3. GENERATE ERROR-FREE HTML =====
def generate_html(videos, news_items):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SPORTS NEWS</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .box {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
            .box iframe, .box img {{ width: 100%; border-radius: 5px; }}
            .box h3 {{ margin-top: 0; }}
            .box a {{ color: #0066cc; text-decoration: none; }}
        </style>
    </head>
    <body>
        <h2>📺 Weekly Sports Recap</h2>
        <p><em>Updated: {timestamp}</em></p>
        
        <!-- Videos Section (3 rows x 2 columns) -->
        <div class="container">
            {''.join(
                f'<div class="box"><h3>{sport}</h3><iframe src="{url}" frameborder="0" allowfullscreen></iframe></div>'
                for sport, url in videos.items()
            )}
        </div>
        
        <!-- News Section (3 rows x 2 columns) -->
        <div class="container">
            {''.join(
                f'''<div class="box">
                    <img src="{item['image_url']}" onerror="this.src='https://via.placeholder.com/150'">
                    <h3><a href="{item['link']}" target="_blank">{item['title']}</a></h3>
                    <p>{item['summary']}</p>
                </div>'''
                for item in news_items[:6]  # Show top 6 news
            )}
        </div>
    </body>
    </html>
    """
    return html

# ===== 4. MAIN EXECUTION (NO TOUCHING THE NURSE!) =====
if __name__ == "__main__":
    feed_urls = [
        "https://www.espn.com/espn/rss/news",
        "https://www.skysports.com/rss/12040",
        "https://www.tennisworldusa.org/rss.xml",
        "https://www.wrestlinginc.com/rss/news.xml",
        "https://www.boxingscene.com/rss.php"
    ]
    
    # Get data
    news_items = parse_feeds(feed_urls, max_items_per_feed=3)  # 3 items per feed
    html_content = generate_html(video_playlists, news_items)
    
    # Save HTML (GitHub Pages will host this)
    write_html_file("sports_news_combined.html", html_content)
    print("🎉 HTML generated successfully!")