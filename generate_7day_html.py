from _common import parse_feeds_and_generate_html, write_html_file

feed_urls = [
    "https://www.dawn.com/feeds/home",
    "https://tribune.com.pk/feed",
    "https://www.brecorder.com/rss/rss.xml",
]

html_content = parse_feeds_and_generate_html(
    feed_urls=feed_urls,
    hours_limit=168,  # 7 days
    max_items=50,
    section_title="News Archive – Past 7 Days"
)

write_html_file("news_7day.html", html_content)
