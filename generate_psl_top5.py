from googleapiclient.discovery import build
from _common import write_html_file

# ✅ USING VALID YOUTUBE API KEY
api_key = "AIzaSyADRyWjUl0xfBVCkW8r-3YoM_72e5Qso2c"
youtube = build("youtube", "v3", developerKey=api_key)

request = youtube.search().list(
    q="PSL 2025 Highlights",
    part="snippet",
    type="video",
    maxResults=5
)
response = request.execute()

html = "<h2>🔥 PSL 2025 – Top 5 Highlights</h2>\n"
for item in response.get("items", []):
    video_id = item["id"]["videoId"]
    title = item["snippet"]["title"]
    html += f'<p><b>{title}</b><br><iframe width="100%" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe></p>\n'

write_html_file("news_psl_top5.html", html)
