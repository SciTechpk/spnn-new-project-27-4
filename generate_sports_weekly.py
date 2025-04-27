from _common import parse_feeds_and_generate_html, write_html_file

feed_urls = [
    "https://www.espn.com/espn/rss/news",
    "https://www.skysports.com/rss/12040",
]

html_content = parse_feeds_and_generate_html(
    feed_urls=feed_urls,
    hours_limit=168,
    max_items=15,
    section_title="Top Sports Stories This Week"
)

write_html_file("news_sports_weekly.html", html_content)
