from src.utils.debug_section import debug

class GameState:
    def __init__(self):
        self.current_screen = 'main_menu'
        self.level = 1  # Default level

    def set_screen(self, screen):
        self.current_screen = screen

    def get_screen(self):
        return self.current_screen

    def set_level(self, level):
        """
        Set the current game level
        
        Args:
            level (int): Level to set
        """
        # Ensure level is between 1 and 3
        self.level = max(1, min(level, 3))
        debug.log('game_state', f"Level set to {self.level}")

    def get_level(self):
        """
        Get the current game level
        
        Returns:
            int: Current game level
        """
        return self.level

    def trigger_win_condition(self):
        """
        Handle the logic when a player wins a level.
        """
        debug.log('game_state', f"Player has won level {self.level}")
        self.win_condition_triggered = True

# Create a global instance
current_game_state = GameState()