from _common import parse_feeds_and_generate_html, write_html_file

# Define RSS feed URLs
feed_urls = [
    "https://www.espncricinfo.com/rss/content/story/feeds/0.xml",  # ESPN Cricinfo
    "https://jang.com.pk/rss/latest",  # Jang News
    "https://www.express.pk/feed/",  # Express News
    "https://www.nawaiwaqt.com.pk/rss/latest"  # Nawa-e-Waqt
]

# Generate HTML content from RSS feeds
html_content = parse_feeds_and_generate_html(
    feed_urls=feed_urls,
    hours_limit=48,
    keywords=["PSL", "Pakistan Super League", "Multan", "Lahore", "Karachi", "Islamabad"],
    max_items=2,  # Limit to 2 news items
    section_title="PSL 2025 – Live Coverage"
)

# Write the generated HTML content to the output file
write_html_file("news_psl_live.html", html_content)