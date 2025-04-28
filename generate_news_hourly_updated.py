import feedparser
from datetime import datetime

# Define RSS feed URLs for all 11 sources
RSS_FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "Reuters": "http://feeds.reuters.com/reuters/topNews",
    "DW": "https://rss.dw.com/xml/rss-en-all",
    "AP": "https://apnews.com/rss",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "Fox News": "https://moxie.foxnews.com/feedburner/latest.xml",
    "Dawn": "https://www.dawn.com/feed",
    "Jang": "https://jang.com.pk/rss",  # RSS feed for Jang
    "Express": "https://express.pk/rss",  # RSS feed for Express
    "Business Recorder": "https://www.brecorder.com/feed",  # RSS feed for Business Recorder
    "TRT": "https://www.trtworld.com/rss",  # RSS feed for TRT
}

# Function to fetch and parse RSS feed
def fetch_feed(url):
    try:
        feed = feedparser.parse(url)
        entries = feed.entries[:2]  # Fetch only the first 2 entries per feed
        return entries
    except Exception as e:
        print(f"Error fetching feed from {url}: {e}")
        return []

# Generate HTML content
def generate_html():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hourly Updated News</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #d5f7d5; /* Light green background - untouched */
            margin: 20px;
        }
        h1 {
            text-align: center;
            color: black;
        }
        .timestamp {
            text-align: center;
            color: #555;
            font-size: 0.9em;
            margin-bottom: 30px;
        }
        .news-container {
            display: flex;
            flex-direction: column;
            gap: 30px;
        }
        .news-item {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px #ccc;
        }
        .news-item img {
            max-width: 150px; /* Resized to 2 inches width */
            height: auto;
            margin-top: 10px;
            border-radius: 8px;
        }
        .news-item h2 {
            color: #0074cc; /* Blue colored title */
            font-size: 1.5em;
            cursor: pointer;
            transition: color 0.3s ease;
        }
        .news-item h2:hover {
            color: #ff6347; /* Change color on hover */
            text-decoration: underline; /* Underline on hover */
        }
        .news-item p {
            color: #222; /* Black summary */
        }
    </style>
</head>
<body>
    <h1>🕒 Hourly Updated News Feed</h1>
    <div class="timestamp">Last updated: {} UTC</div>
    <div class="news-container">
""".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

    # Fetch news items from all RSS feeds
    for source, url in RSS_FEEDS.items():
        entries = fetch_feed(url)
        for entry in entries:
            # Extract title, link, and summary
            title = entry.title if hasattr(entry, "title") else "No Title"
            link = entry.link if hasattr(entry, "link") else "#"
            summary = entry.summary if hasattr(entry, "summary") else "No summary available."

            # Extract image URL if available
            image_url = "#"
            if hasattr(entry, "media_content") and len(entry.media_content) > 0:
                image_url = entry.media_content[0]["url"]
            elif hasattr(entry, "enclosures") and len(entry.enclosures) > 0:
                image_url = entry.enclosures[0].href

            # Add news item to HTML content
            html_content += f"""
        <div class="news-item">
            <a href="{link}" target="_blank" rel="noopener noreferrer">
                <h2>{title}</h2>
            </a>
            <p>{summary}</p>
            <img src="{image_url}" alt="{title}" onerror="this.style.display='none';">
        </div>
"""

    # Close HTML tags
    html_content += """
    </div>
</body>
</html>
"""

    # Write the generated HTML to a file
    with open("news_hourly_updated.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("HTML file 'news_hourly_updated.html' has been successfully generated.")

# Run the script
if __name__ == "__main__":
    generate_html()