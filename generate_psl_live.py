from _common import parse_feeds_and_generate_html, write_html_file

feed_urls = [
    "https://www.espncricinfo.com/rss/content/story/feeds/0.xml",
]

html_content = parse_feeds_and_generate_html(
    feed_urls=feed_urls,
    hours_limit=48,
    keywords=["PSL", "Pakistan Super League", "Multan", "Lahore", "Karachi", "Islamabad"],
    max_items=20,
    section_title="PSL 2025 – Live Coverage"
)

write_html_file("news_psl_live.html", html_content)
