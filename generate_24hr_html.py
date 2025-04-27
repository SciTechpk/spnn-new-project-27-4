from _common import parse_feeds_and_generate_html, write_html_file

feed_urls = [
    "https://www.dawn.com/feeds/home",
    "https://tribune.com.pk/feed",
    "https://www.brecorder.com/rss/rss.xml",
    "https://www.geo.tv/rss/1/1",
    "https://jang.com.pk/rss/english.xml",
]

html_content = parse_feeds_and_generate_html(
    feed_urls=feed_urls,
    hours_limit=24,
    max_items=40,
    section_title="News Archive – 24 Hours"
)

write_html_file("news_24hr.html", html_content)
