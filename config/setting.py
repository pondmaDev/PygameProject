import json
from typing import Any, Dict

class Setting:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Setting, cls).__new__(cls)
            cls._instance.init_settings()
        return cls._instance

    def init_settings(self):
        """Initialize default settings with direct attributes"""
        # Default settings as direct attributes
        self.bg_music_volume = 50
        self.sound_effects_volume = 50
        self.window_mode = True
        self.character_speed = 1.0
        self.difficulty = 'medium'
        
        # Keep the settings dictionary for backward compatibility
        self.settings = {
            'bg_music_volume': self.bg_music_volume,
            'window_mode': self.window_mode,
            'character_speed': self.character_speed,
            'sound_effects_volume': self.sound_effects_volume,
            'difficulty': self.difficulty
        }

        self.LEVEL_SCROLL_MULTIPLIERS = {
            1: 1.0,   # Base speed
            2: 1.2,   # Slightly faster
            3: 1.5,   # Faster
            4: 1.8,   # Much faster
            5: 2.0    # Maximum speed
        }
    
    def get_level_scroll_multiplier(self, level):
        """
        Get scroll multiplier for a specific level
        
        Args:
            level (int): Game level
        
        Returns:
            float: Scroll speed multiplier
        """
        return self.LEVEL_SCROLL_MULTIPLIERS.get(level, 1.0)  # Default to 1.0 if level not found

    def load_settings(self, file_path: str) -> None:
        """Load settings from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                loaded_settings = json.load(file)
                
                # Update both direct attributes and settings dictionary
                for key, value in loaded_settings.items():
                    setattr(self, key, value)
                    self.settings[key] = value
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading settings: {e}")

    def save_settings(self, file_path: str) -> None:
        """Save current settings to a JSON file."""
        # Ensure settings dictionary is up to date
        self.settings.update({
            'bg_music_volume': self.bg_music_volume,
            'window_mode': self.window_mode,
            'character_speed': self.character_speed,
            'sound_effects_volume': self.sound_effects_volume,
            'difficulty': self.difficulty
        })
        
        with open(file_path, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def adjust_bg_music_volume(self, new_volume: int) -> None:
        """Adjust background music volume."""
        self.bg_music_volume = max(0, min(100, new_volume))
        self.settings['bg_music_volume'] = self.bg_music_volume

    def toggle_window_mode(self) -> None:
        """Toggle between windowed and fullscreen mode."""
        self.window_mode = not self.window_mode
        self.settings['window_mode'] = self.window_mode

    def adjust_character_speed(self, new_speed: float) -> None:
        """Adjust character speed."""
        self.character_speed = max(0, min(10, round(new_speed, 1)))
        self.settings['character_speed'] = self.character_speed

    def get_setting(self, key: str) -> Any:
        """Get a specific setting."""
        return getattr(self, key, None)

    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access"""
        return getattr(self, key, None)

# Create a global instance
current_settings = Setting()