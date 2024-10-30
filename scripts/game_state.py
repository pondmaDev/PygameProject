# scripts/game_state.py
class GameState:
    def __init__(self):
        self.current_screen = 'main_menu'
        self.level = None

    def set_screen(self, screen):
        self.current_screen = screen

    def get_screen(self):
        return self.current_screen

    def set_level(self, level):
        self.level = level

    def get_level(self):
        return self.level

# Create a global instance
current_game_state = GameState()