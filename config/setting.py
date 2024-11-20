import json
import os
import logging
from typing import Any, Dict

class SettingsLogger:
    """Enhanced logging for settings management"""
    def __init__(self, log_file='logs/settings.log'):
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Configure logging
        self.logger = logging.getLogger('SettingsManager')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)

class Settings:
    """Enhanced settings management with comprehensive configuration"""
    _instance = None
    _logger = SettingsLogger()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._initialize_settings()
        return cls._instance

    def _initialize_settings(self):
        self.setting_validations = {
            'bg_music_volume': {
                'min': 0, 
                'max': 100, 
                'type': int,
                'description': 'Background music volume (0-100)'
            },
            'sound_effects_volume': {
                'min': 0, 
                'max': 100, 
                'type': int,
                'description': 'Sound effects volume (0-100)'
            }
        }

        # Audio Settings
        self.bg_music_volume = 50
        self.sound_effects_volume = 50
        
        # Gameplay Settings
        self.character_speed = 1.0
        self.difficulty = 'medium'
        self.show_fps = False
        
        # Add level scroll multiplier
        self.level_scroll_multiplier = 1.0
        
        # Add validation for level scroll multiplier
        self.setting_validations['level_scroll_multiplier'] = {
            'min': 0.1,  # Minimum scroll speed
            'max': 3.0,  # Maximum scroll speed 
            'type': float,
            'description': 'World scroll speed multiplier (0.1-3.0)'
        }
        
        # Control Settings
        self.key_bindings = {
            'move_up': 'W',
            'move_down': 'S',
            'move_left': 'A', 
            'move_right': 'D'
        }
        
        # Accessibility Settings
        self.color_blind_mode = False
        self.text_size = 'medium'
        
        # Settings file path
        self.settings_file_path = 'config/user_settings.json'


    def get_level_scroll_multiplier(self, level: int = 1):
        """
        Get the current level scroll multiplier.
        
        Args:
            level (int, optional): Current game level. Defaults to 1.
        
        Returns:
            float: Current scroll speed multiplier
        """
        # Optional: Implement level-based scaling if desired
        base_multiplier = getattr(self, 'level_scroll_multiplier', 1.0)
        
        # Simple linear scaling (optional)
        # You can customize this scaling logic as needed
        level_scaling_factor = 1 + (level - 1) * 0.1  # Increases by 10% per level
        
        return base_multiplier * level_scaling_factor

    def set_level_scroll_multiplier(self, multiplier):
        """
        Set the level scroll multiplier with validation.
        
        Args:
            multiplier (float): Desired scroll speed multiplier
        
        Returns:
            float: Validated and set multiplier
        """
        try:
            # Use existing validation method
            validated_multiplier = self.validate_setting(
                'level_scroll_multiplier', 
                multiplier
            )
            
            # Set the validated multiplier
            self.level_scroll_multiplier = validated_multiplier
            
            # Log the change
            self._logger.info(f"Level scroll multiplier set to {validated_multiplier}")
            
            return validated_multiplier
        except Exception as e:
            # Fallback to default if setting fails
            self._logger.error(f"Error setting scroll multiplier: {e}")
            self.level_scroll_multiplier = 1.0
            return 1.0

    def reset_level_scroll_multiplier(self):
        """
        Reset the level scroll multiplier to default (1.0)
        """
        self.level_scroll_multiplier = 1.0
        self._logger.info("Level scroll multiplier reset to default")

    def save(self, file_path=None):
        """
        Save settings to a file.
        If no file path is provided, use the default settings file path.
        """
        try:
            # Use the default settings file path if not provided
            if file_path is None:
                file_path = self.settings_file_path
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Call the extended save_settings method
            self.save_settings(file_path)
            
            # Log successful save
            self._logger.info(f"Settings saved to {file_path}")
        except Exception as e:
            # Log the error
            self._logger.error(f"Error saving settings: {e}")
            print(f"Error saving settings: {e}")

    def load(self, file_path):
        """
        Load settings from a file.
        """
        try:
            # Call the extended load_settings method
            self.load_settings(file_path)
        except Exception as e:
            print(f"Error loading settings: {e}")

    # Update save_settings to include new multiplier
    def save_settings(self, file_path=None):
        """
        Extended save_settings to ensure new settings are saved
        """
        settings_data = {
            'level_scroll_multiplier': self.level_scroll_multiplier,
            # Add other settings attributes here
        }
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(settings_data, f)
        else:
            # Handle the case where no file_path is provided
            print("No file path provided for saving settings.")

    def load_settings(self, file_path=None):
        """
        Extended load_settings to handle new multiplier setting
        """
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    settings_data = json.load(f)
                    self.level_scroll_multiplier = settings_data.get('level_scroll_multiplier', 1.0)
                    # Load other settings attributes here
            except FileNotFoundError:
                print("Settings file not found.")
            except json.JSONDecodeError:
                print("Error decoding JSON from settings file.")
        else:
            # Handle the case where no file_path is provided
            print("No file path provided for loading settings.")

    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self._initialize_settings()
        self._logger.info("Settings reset to default values")

    def validate_setting(self, key, value):
        """Validate a specific setting"""
        if key in self.setting_validations:
            config = self.setting_validations[key]
            try:
                # Convert and clamp value
                converted_value = config['type'](value)
                return max(config['min'], min(converted_value, config['max']))
            except (ValueError, TypeError):
                self._logger.warning(f"Invalid value for {key}: {value}")
                return getattr(self, key)  # Return current value if invalid
        return value

# Global settings instance
current_settings = Settings()