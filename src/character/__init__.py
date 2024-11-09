# Import specific character classes you want to make easily accessible
from .character import Character
from .character_controller import CharacterController

# Optional: Define what gets imported when someone does "from characters import *"
__all__ = ['Character', 'CharacterController']