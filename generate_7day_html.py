import feedparser
from _common import write_html_file

# Updated list of RSS feed URLs
feed_urls = [
    "https://www.dawn.com/feeds/home",
    "https://www.thenews.com.pk/rss/1/1",  # Replacement for Jang
    "https://dailytimes.com.pk/feed/",    # Replacement for AP
    "https://www.geo.tv/rss/1/1",
    "https://www.bbc.com/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://moxie.foxnews.com/feedburner/latest.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.theguardian.com/world/rss"
]

# Function to parse feeds and extract top N items per feed
def parse_feeds(feed_urls, max_items_per_feed):
    all_news_items = []
    for feed_url in feed_urls:
        try:
            print(f"Processing feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            print(f"Number of entries found: {len(feed.entries)}")
            for entry in feed.entries[:max_items_per_feed]:
                title = entry.title if hasattr(entry, 'title') else "No Title"
                summary = entry.summary if hasattr(entry, 'summary') else "No Summary Available"
                truncated_summary = (summary[:150] + "...") if len(summary) > 150 else summary
                link = entry.link if hasattr(entry, 'link') else "#"
                image_url = "#"
                if hasattr(entry, 'media_content') and len(entry.media_content) > 0:
                    image_url = entry.media_content[0]['url']
                elif hasattr(entry, 'enclosures') and len(entry.enclosures) > 0:
                    image_url = entry.enclosures[0].href
                all_news_items.append({
                    "title": title,
                    "summary": truncated_summary,
                    "link": link,
                    "image_url": image_url
                })
        except Exception as e:
            print(f"Error processing feed {feed_url}: {e}")
    return all_news_items

# Generate HTML content
def generate_html(news_items):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>News Archive – Past 7 Days</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
                background-color: #f9f9f9;
            }
            h2 {
                color: #333;
                text-align: center;
            }
            .news-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: space-between;
            }
            .news-item {
                background: #fff;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 15px;
                width: calc(20% - 20px); /* 5 boxes per row */
                box-sizing: border-box;
            }
            .news-item img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                margin-bottom: 10px;
            }
            .news-item a {
                text-decoration: none;
                color: #007BFF;
            }
            .news-item a:hover {
                text-decoration: underline;
            }
            small {
                color: #666;
                display: block;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h2>News Archive – Past 7 Days</h2>
        <div class="news-container">
    """
    for item in news_items:
        html += f"""
        <div class="news-item">
            <img src='{item["image_url"]}' alt='News Image' onerror="this.src='https://via.placeholder.com/150'; this.onerror=null;">
            <a href='{item["link"]}' target='_blank'><strong>{item["title"]}</strong></a>
            <p>{item["summary"]}</p>
            <small><a href='{item["link"]}' target='_blank'>Read More</a></small>
        </div>
        """
    html += "</div></body></html>"
    return html

# Main execution
if __name__ == "__main__":
    max_items_per_feed = 5  # For news_7day.html
    news_items = parse_feeds(feed_urls, max_items_per_feed)
    print(f"Total news items extracted: {len(news_items)}")
    html_content = generate_html(news_items)
    write_html_file("news_7day.html", html_content)