# _common.py
import feedparser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def clean_html(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text()

def parse_feeds_and_generate_html(feed_urls, hours_limit=None, max_items=None, keywords=None, section_title=None):
    now = datetime.utcnow()
    all_items = []

    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = getattr(entry, 'published_parsed', None)
            if not published:
                continue
            published_dt = datetime(*published[:6])
            if hours_limit:
                if (now - published_dt) > timedelta(hours=hours_limit):
                    continue
            title = entry.get("title", "")
            summary = clean_html(entry.get("summary", ""))
            link = entry.get("link", "")
            image = ""
            media_content = entry.get("media_content", [])
            if media_content:
                image = media_content[0].get("url", "")
            if keywords:
                if not any(kw.lower() in title.lower() + summary.lower() for kw in keywords):
                    continue
            all_items.append({
                "title": title,
                "summary": summary,
                "link": link,
                "image": image,
                "published": published_dt,
            })

    all_items.sort(key=lambda x: x["published"], reverse=True)
    if max_items:
        all_items = all_items[:max_items]

    html = f"<h2>{section_title}</h2>\n" if section_title else ""
    for item in all_items:
        html += f"<div style='margin-bottom:20px;'>"
        if item['image']:
            html += f"<img src='{item['image']}' width='100%'><br>"
        html += f"<a href='{item['link']}' target='_blank'><strong>{item['title']}</strong></a><br>"
        html += f"<p>{item['summary']}</p>"
        html += f"<small>{item['published'].strftime('%Y-%m-%d %H:%M')}</small>"
        html += "</div><hr>"

    return html

def write_html_file(filename, content, marker=None):
    if marker:
        content = f"<!-- {marker} START -->\n{content}\n<!-- {marker} END -->"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
