import os
from googleapiclient.discovery import build
from _common import write_html_file

# Fetch YouTube API key from environment variable
api_key = os.getenv("YOUTUBE_API_KEY")
if not api_key:
    raise ValueError("YouTube API key not found in environment variables.")

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

# Fetch top 5 PSL 2025 highlights
request = youtube.search().list(
    q="PSL 2025 Highlights",
    part="snippet",
    type="video",
    maxResults=5
)
response = request.execute()

# Generate HTML content
html = "<h2>🔥 PSL 2025 – Top 5 Highlights</h2>\n"
for item in response.get("items", []):
    video_id = item["id"]["videoId"]
    title = item["snippet"]["title"]
    html += f'<p><b>{title}</b><br><iframe width="100%" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe></p>\n'

# Write HTML content to file
write_html_file("news_psl_top5.html", html)