import random
from datetime import datetime

def get_rotated_playlists():
    """Deterministic 30-min rotation - No randomness, no flickering"""
    ALL_SPORTS = {
        "Cricket": "https://www.youtube.com/embed/videoseries?list=PLl6h6UvLNv39Tguhu-5xKTz1-egoPwlZ0",
        "Boxing": "https://www.youtube.com/embed/videoseries?list=PL-KAIrL6czM_bnmP8z41QdEVCXcj0UjEA",
        "Tennis": "https://www.youtube.com/embed/videoseries?list=PLiDzi8ftbdotLBZnLcM42tHlc0D0FNEvk",
        "Football": "https://www.youtube.com/embed/videoseries?list=PLV3zWUbtkFC3mEBBsTdlQ59hiQEo_WuOT",
        "Soccer": "https://www.youtube.com/embed/videoseries?list=PLnaYFo37eXKUvS-SkkgHbMiKxFky4J7IX",
        "Wrestling": "https://www.youtube.com/embed/videoseries?list=PL51olEIebDW0IoUNpWzeBcS16XryrnpBj"
    }
    
    # Calculate stable rotation index (changes every 30 mins)
    interval_num = int(datetime.now().timestamp() // (30 * 60))  # 30-min blocks
    start_idx = interval_num % len(ALL_SPORTS)
    
    # Get 6 sequential sports (wraps if needed)
    rotated_items = list(ALL_SPORTS.items())[start_idx:] + list(ALL_SPORTS.items())[:start_idx]
    return dict(rotated_items[:6])  # Always return exactly 6

# Optional: Test rotation stability
if __name__ == "__main__":
    print("Current rotation:", list(get_rotated_playlists().keys()))