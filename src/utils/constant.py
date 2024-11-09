

class Colors:
    # Define color codes as a dictionary
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    GRAY_HOVER = (125, 123,164)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)

    @classmethod
    def get(cls, color_name):
        """
        Get color by name, case-insensitive
        
        Args:
            color_name (str): Name of the color
        
        Returns:
            tuple: RGB color tuple
        """
        try:
            # Convert to uppercase to match class attributes
            return getattr(cls, color_name.upper())
        except AttributeError:
            # Fallback to black if color not found
            print(f"Warning: Color {color_name} not found. Using BLACK.")
            return cls.RED

    @classmethod
    def get_color_name(cls, color_tuple):
        """
        Find color name for a given color tuple
        """
        for name, value in cls.COLORS.items():
            if value == color_tuple:
                return name
        return 'RED'

class ButtonDimensions:
    WIDTH = 200
    HEIGHT = 50

# Timing
CLICK_DELAY = 300
FPS = 60
#background

# Font sizes
TITLE_FONT_SIZE = 74
BUTTON_FONT_SIZE = 30

#Speed
MIN_SPEED = 1.0
MAX_SPEED = 10.0
SPEED_INCREMENT = 1.0  # Amount to increase or decrease speed