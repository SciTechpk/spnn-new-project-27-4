from _common import parse_feeds_and_generate_html, write_html_file

feed_urls = [
    "https://www.espn.com/espn/rss/news",
    "https://www.skysports.com/rss/12040",
]

html_content = parse_feeds_and_generate_html(
    feed_urls=feed_urls,
    hours_limit=24,
    max_items=5,
    keywords=["cricket", "football", "tennis", "goal", "six", "run", "match", "tournament"],
    section_title="Top 5 Sports Highlights Today"
)

write_html_file("news_top5_sports.html", html_content)
