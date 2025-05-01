# video_rotation_engine.py
import random
from datetime import datetime

def get_rotated_playlists():
    """AUTOMATIC rotation with every run - SAFE and CONSISTENT"""
    ALL_SPORTS = {
        "Cricket": "https://www.youtube.com/embed/videoseries?list=PLl6h6UvLNv39Tguhu-5xKTz1-egoPwlZ0",
        "Boxing": "https://www.youtube.com/embed/videoseries?list=PL-KAIrL6czM_bnmP8z41QdEVCXcj0UjEA",
        "Tennis": "https://www.youtube.com/embed/videoseries?list=PLiDzi8ftbdotLBZnLcM42tHlc0D0FNEvk",
        "Football": "https://www.youtube.com/embed/videoseries?list=PLV3zWUbtkFC3mEBBsTdlQ59hiQEo_WuOT",
        "Soccer": "https://www.youtube.com/embed/videoseries?list=PLnaYFo37eXKUvS-SkkgHbMiKxFky4J7IX",
        "Wrestling": "https://www.youtube.com/embed/videoseries?list=PL51olEIebDW0IoUNpWzeBcS16XryrnpBj"
    }
    
    # Seed random with weekly timestamp for consistent weekly rotation
    random.seed(datetime.now().isocalendar()[1])
    return dict(random.sample(list(ALL_SPORTS.items()), k=3))  # Returns 3 random sports

# TEST: Uncomment to verify
# print("This run's sports:", get_rotated_playlists().keys())