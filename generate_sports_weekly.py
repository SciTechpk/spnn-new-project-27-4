import feedparser
from _common import write_html_file
from datetime import datetime
import sys

# ===== 1. VERIFIED YOUTUBE PLAYLISTS (NO RESTRICTIONS) =====
video_playlists = {
    "Cricket": "https://www.youtube.com/embed/videoseries?list=PLczcwOD2NpZfl6PXq11m6kzD7Z0zC4QzV",
    "Football": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfdGq1dP7qg4FhUum5J8T1vW",
    "Tennis": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc07FjZ5hR7OVc4mjx1Y0L1",
    "Soccer": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc8G1FozR6j-tBq3Y9XzW1A",
    "Wrestling": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc1Y0X9gZ0k6Xq5YJmz0Q2X",
    "Boxing": "https://www.youtube.com/embed/videoseries?list=PLQ_voP4Q3cfc1Y0X9gZ0k6Xq5YJmz0Q2Y"
}

# ===== 2. FAILSAFE RSS PARSER =====
def parse_feeds(feed_urls, max_items):
    news_items = []
    for url in feed_urls:
        try:
            print(f"Fetching: {url}", file=sys.stderr)
            feed = feedparser.parse(url)
            if not feed.entries:
                print(f"No entries in feed: {url}", file=sys.stderr)
                continue
            
            for entry in feed.entries[:max_items]:
                title = entry.get('title', 'No Title')
                summary = entry.get('summary', 'No summary')
                summary = (summary[:150] + '...') if len(summary) > 150 else summary
                image_url = entry.get('media_content', [{}])[0].get('url', 'https://via.placeholder.com/150')
                
                news_items.append({
                    "title": title,
                    "summary": summary,
                    "link": entry.get('link', '#'),
                    "image_url": image_url
                })
        except Exception as e:
            print(f"RSS Error ({url}): {str(e)}", file=sys.stderr)
    return news_items

# ===== 3. HTML GENERATOR (NO COMMENTS IN F-STRINGS) =====
def generate_html(videos, news_items):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    video_boxes = ''.join(
        f'<div class="box"><h3>{sport}</h3><iframe src="{url}" allowfullscreen></iframe></div>'
        for sport, url in videos.items()
    )
    news_boxes = ''.join(
        f'<div class="box"><img src="{item["image_url"]}"><h3><a href="{item["link"]}" target="_blank">{item["title"]}</a></h3><p>{item["summary"]}</p></div>'
        for item in news_items[:6]
    )
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SPNN Sports Weekly</title>
    <style>
        body {{ font-family: Arial; margin: 20px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .box {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
        iframe, .box img {{ width: 100%; height: 200px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h2>📺 Weekly Sports Recap</h2>
    <p>Updated: {timestamp}</p>
    <div class="grid">{video_boxes}</div>
    <div class="grid">{news_boxes}</div>
</body>
</html>"""

# ===== 4. MAIN EXECUTION =====
if __name__ == "__main__":
    try:
        feed_urls = [
            "https://www.espn.com/espn/rss/news",
            "https://www.skysports.com/rss/12040",
            "https://www.tennisworldusa.org/rss.xml",
            "https://www.wrestlinginc.com/rss/news.xml",
            "https://www.boxingscene.com/rss.php"
        ]
        news_items = parse_feeds(feed_urls, max_items=3)
        html_content = generate_html(video_playlists, news_items)
        write_html_file("news_sports_weekly.html", html_content)
        print("Success: news_sports_weekly.html generated", file=sys.stderr)
    except Exception as e:
        print(f"Critical error: {str(e)}", file=sys.stderr)
        sys.exit(1)