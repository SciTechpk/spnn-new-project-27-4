import feedparser
from _common import write_html_file

# YouTube Playlist URLs
video_playlists = {
    "Cricket": "https://www.youtube.com/embed/PlepeKf7U6gmbOZHauY5-WDhE9HBZkJde0?index=2",
    "Football": "https://www.youtube.com/embed/PLCGIzmTE4d0gkjAit8YW-Wp1p9HceS-Cz?index=1",
    "Tennis": "https://www.youtube.com/embed/PL56Rm_uKfHfpdIg7mUo7Dd_YxadtBhdYq?index=1",
    "Soccer": "https://www.youtube.com/embed/PLjF76OEQArJfZv1vdC6YW0uQHXG2P7zQH?index=1",
    "Wrestling": "https://www.youtube.com/embed/PL6_ns0hIFOCGH5VKPsEoqU188Xx3gzwwS?index=1",
    "Boxing": "https://www.youtube.com/embed/PL-KAIrL6czM9XywYqaXGezYQmXeOv-_Hc?index=1"
}

# RSS Feed URLs for Sports News
feed_urls = [
    "https://www.espn.com/espn/rss/news",
    "https://www.skysports.com/rss/12040",
    "https://www.tennisworldusa.org/rss.xml",
    "https://www.wrestlinginc.com/rss/news.xml",
    "https://www.boxingscene.com/rss.php"
]

# Function to parse feeds and extract top N items per feed
def parse_feeds(feed_urls, max_items_per_feed):
    all_news_items = []
    for feed_url in feed_urls:
        try:
            feed = feedparser.parse(feed_url)
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
def generate_html(videos, news_items):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weekly Sports Recap</title>
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
            .container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: space-between;
            }
            .box {
                background: #fff;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 15px;
                width: calc(33% - 20px); /* 3 boxes per row */
                box-sizing: border-box;
            }
            .box iframe {
                width: 100%;
                height: 200px;
                border: none;
                border-radius: 8px;
            }
            .box img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                margin-bottom: 10px;
            }
            .box a {
                text-decoration: none;
                color: #007BFF;
            }
            .box a:hover {
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
        <h2>📺 Weekly Sports Recap</h2>
        <p><em>Updated: 2025-04-28 15:53 UTC</em></p>
        <div class="container">
    """
    # Add video boxes
    for sport, video_url in videos.items():
        html += f"""
        <div class="box">
            <h3>{sport} Highlights</h3>
            <iframe src='{video_url}' frameborder='0' allowfullscreen></iframe>
        </div>
        """
    
    # Add news boxes
    for item in news_items:
        html += f"""
        <div class="box">
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
    max_items_per_feed = 2  # 2 news items per feed
    news_items = parse_feeds(feed_urls, max_items_per_feed)
    html_content = generate_html(video_playlists, news_items)
    write_html_file("news_sports_weekly.html", html_content)