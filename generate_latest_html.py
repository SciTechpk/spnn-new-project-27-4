import feedparser
from bs4 import BeautifulSoup
from datetime import datetime

feed_urls = [
    "https://arynews.tv/feed/",
    "https://jang.com.pk/rss/",
    "https://www.dawn.com/rss",
    "https://www.brecorder.com/rss",
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://rss.cnn.com/rss/edition.rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.dawn.com/feeds/home",
    "https://tribune.com.pk/feed",
]

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def fetch_feed_items(feed_url, max_items=5):
    feed = feedparser.parse(feed_url)
    items = []
    for entry in feed.entries[:max_items]:
        title = clean_html(entry.title)
        link = entry.link
        published = entry.get("published", "No date")
        items.append(f"<li><a href='{link}' target='_blank'>{title}</a> <small>({published})</small></li>")
    return items

all_items = []
for url in feed_urls:
    try:
        items = fetch_feed_items(url, max_items=3)
        all_items.extend(items)
    except Exception as e:
        print(f"Error with feed {url}: {e}")

timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SPNN - Hourly Updated News</title>
</head>
<body>
    <h2>🕒 Hourly Updated News Feed</h2>
    <p><em>Last updated: {timestamp}</em></p>
    <ul>
        {''.join(all_items)}
    </ul>
</body>
</html>
"""

with open("news_latest.html", "w", encoding="utf-8") as f:
    f.write(html_content)
