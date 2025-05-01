# video_rotator.py (STANDALONE - NO IMPORTS NEEDED)
from datetime import datetime

def get_rotated_sports():
    """Predictable weekly rotation using date math"""
    SPORTS_PLAYLISTS = {
        # YOUR ORIGINAL PLAYLISTS (COPY-PASTE FROM WORKING SCRIPT)
        "Cricket": "https://www.youtube.com/embed/videoseries?list=PLl6h6UvLNv39Tguhu-5xKTz1-egoPwlZ0",
        "Boxing": "https://www.youtube.com/embed/videoseries?list=PL-KAIrL6czM_bnmP8z41QdEVCXcj0UjEA",
        "Tennis": "https://www.youtube.com/embed/videoseries?list=PLiDzi8ftbdotLBZnLcM42tHlc0D0FNEvk",
        "Football": "https://www.youtube.com/embed/videoseries?list=PLV3zWUbtkFC3mEBBsTdlQ59hiQEo_WuOT",
        "Soccer": "https://www.youtube.com/embed/videoseries?list=PLnaYFo37eXKUvS-SkkgHbMiKxFky4J7IX",
        "Wrestling": "https://www.youtube.com/embed/videoseries?list=PL51olEIebDW0IoUNpWzeBcS16XryrnpBj"
    }
    
    # Weekly rotation algorithm (no randomness)
    week_num = datetime.now().isocalendar()[1]  # ISO week number
    start_idx = week_num % len(SPORTS_PLAYLISTS)
    rotated = dict(list(SPORTS_PLAYLISTS.items())[start_idx:] + 
                 list(SPORTS_PLAYLISTS.items())[:start_idx])
    
    return {k: rotated[k] for k in list(rotated)[:4]}  # Return first 4 sports

# Test the rotation
if __name__ == "__main__":
    print("This week's sports:", get_rotated_sports().keys())