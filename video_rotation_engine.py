from datetime import datetime

def get_rotated_playlists():
    """Stable 6-video rotation with pre-rendered HTML to prevent flickering"""
    ALL_SPORTS = {
        "Cricket": "https://www.youtube.com/embed/videoseries?list=PLl6h6UvLNv39Tguhu-5xKTz1-egoPwlZ0",
        "Boxing": "https://www.youtube.com/embed/videoseries?list=PL-KAIrL6czM_bnmP8z41QdEVCXcj0UjEA",
        "Tennis": "https://www.youtube.com/embed/videoseries?list=PLiDzi8ftbdotLBZnLcM42tHlc0D0FNEvk",
        "Football": "https://www.youtube.com/embed/videoseries?list=PLV3zWUbtkFC3mEBBsTdlQ59hiQEo_WuOT",
        "Soccer": "https://www.youtube.com/embed/videoseries?list=PLnaYFo37eXKUvS-SkkgHbMiKxFky4J7IX",
        "Wrestling": "https://www.youtube.com/embed/videoseries?list=PL51olEIebDW0IoUNpWzeBcS16XryrnpBj"
    }

    # 1. Get stable rotation order (no randomness)
    interval_num = int(datetime.now().timestamp() // 1800)  # 30-minute blocks
    start_idx = interval_num % len(ALL_SPORTS)
    sports_items = list(ALL_SPORTS.items())
    rotated = sports_items[start_idx:] + sports_items[:start_idx]

    # 2. Pre-render HTML to prevent DOM reflow
    html_boxes = []
    for sport, url in rotated[:6]:  # Always 6 videos
        html_boxes.append(
            f'''<div class="box" data-loaded="true">
                <h3>{sport}</h3>
                <iframe src="{url}" loading="eager" frameborder="0" allowfullscreen></iframe>
            </div>'''
        )
    
    # 3. Return joined HTML to prevent incremental rendering
    return "".join(html_boxes)