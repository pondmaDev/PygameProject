"""
This module initializes the game package and exposes key components.
"""

# Explicitly import the necessary classes and functions
from .interface import Menu, MainMenu, SettingsMenu, LevelSelectionMenu, PauseMenu
from ..character.character import Character  # Assuming you have Character and Enemy classes
from ..character.character_controller import CharacterController # Assuming you have these classes
from ..system.lane_system import LaneManager

# Optionally, you can define an `__all__` list to specify what is exported
__all__ = [
    'Menu',
    'MainMenu',
    'SettingsMenu',
    'LevelSelectionMenu',
    'PauseMenu',
    'Character',
    'CharacterController',
    'LaneManager'
]