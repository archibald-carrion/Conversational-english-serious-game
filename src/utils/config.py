class AppConfig:
    """Configuration settings for the application"""
    
    # Window size options
    WINDOW_SIZES = [
        "800x600",
        "1024x768",
        "1280x720",
        "1366x768",
        "1920x1080"
    ]
    
    # Default settings
    DEFAULT_WINDOW_SIZE = "1280x720"
    DEFAULT_APPEARANCE_MODE = "Dark"
    DEFAULT_COLOR_THEME = "blue"
    
    # Path constants
    ASSETS_PATH = "assets"
    IMAGES_PATH = "assets/images"
    AUDIO_PATH = "assets/audio"
    
    # Game settings
    MAX_ATTEMPTS = 3
    POINTS_FIRST_TRY = 10
    POINTS_SECOND_TRY = 5
    POINTS_THIRD_TRY = 0