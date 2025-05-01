# video_rotation_engine.py
import random
from datetime import datetime

def get_rotated_playlists():
    """ROTATES EVERY 30 MINUTES (not weekly)"""
    ALL_SPORTS = {
        "Cricket": "https://www.youtube.com/embed/videoseries?list=PLl6h6UvLNv39Tguhu-5xKTz1-egoPwlZ0",
        "Boxing": "https://www.youtube.com/embed/videoseries?list=PL-KAIrL6czM_bnmP8z41QdEVCXcj0UjEA",
        "Tennis": "https://www.youtube.com/embed/videoseries?list=PLiDzi8ftbdotLBZnLcM42tHlc0D0FNEvk",
        "Football": "https://www.youtube.com/embed/videoseries?list=PLV3zWUbtkFC3mEBBsTdlQ59hiQEo_WuOT",
        "Soccer": "https://www.youtube.com/embed/videoseries?list=PLnaYFo37eXKUvS-SkkgHbMiKxFky4J7IX",
        "Wrestling": "https://www.youtube.com/embed/videoseries?list=PL51olEIebDW0IoUNpWzeBcS16XryrnpBj"
    }
    
    # Seed changes every 30 minutes (not weekly)
    current_interval = int(datetime.now().timestamp() // (30 * 60))  # 30-minute blocks
    random.seed(current_interval)  # Resets every 30 mins
    return dict(random.sample(list(ALL_SPORTS.items()), k=3))  # Returns 3 random sports

# TEST: This will change outputs every 30 mins
print("Current rotation:", get_rotated_playlists().keys())