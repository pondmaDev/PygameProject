# scripts/setting.py
class Setting:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Setting, cls).__new__(cls)
            cls._instance.init_settings()
        return cls._instance

    def init_settings(self):
        self.bg_music_volume = 50
        self.window_mode = True
        self.character_speed = 1.0

    def adjust_bg_music_volume(self, new_volume):
        self.bg_music_volume = max(0, min(100, new_volume))

    def toggle_window_mode(self):
        self.window_mode = not self.window_mode

    def adjust_character_speed(self, new_speed):
        self.character_speed = max(0, min(10, round(new_speed, 1)))

# Create a global instance
current_settings = Setting()