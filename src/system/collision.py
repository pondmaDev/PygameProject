# src/game/collision.py
import pygame
from typing import List, Optional
from src.character.character import Character
from src.items.item import Item
from src.utils.debug_section import debug
from src.utils.resource_manager import ResourceManager

class CollisionManager:
    @staticmethod
    def check_item_collisions(
        character: Character, 
        items: List[Item]
    ) -> Optional[dict]:
        """
        Check collisions between character and items
        
        Args:
            character (Character): Game character
            items (List[Item]): List of game items
        
        Returns:
            Optional[dict]: Collision result with score change and items to remove
        """

         # Get resource manager instance
        resource_manager = ResourceManager.get_instance()

        if not character:
            return None

        char_rect = pygame.Rect(
            character.x, 
            character.y, 
            character.width, 
            character.height
        )
        
        collision_results = {
            'score_change': 0,
            'items_to_remove': []
        }

        for item in items[:]:
            item_rect = pygame.Rect(
                item.x, 
                item.y, 
                item.size, 
                item.size
            )

            if char_rect.colliderect(item_rect):
                # Calculate score based on item type
                score_change = item.get_points()
                
                # Play sound effect based on item type
                try:
                    if score_change > 0:
                        # Good item collected
                        resource_manager.play_sound('collect_good_item')
                        debug.log('collision', f"Good item collected! Points: {score_change}")
                    else:
                        # Bad item collected
                        resource_manager.play_sound('collect_bad_item')
                        debug.log('collision', f"Bad item collected! Points: {score_change}")
                except Exception as e:
                    debug.error('collision', f"Error playing collision sound: {e}")
                
                debug.log('collision', f"Collision detected! Item points: {score_change}")
                
                collision_results['score_change'] += score_change
                collision_results['items_to_remove'].append(item)

        return collision_results

    @staticmethod
    def is_game_over(current_score: int) -> bool:
        """
        Determine if the game is over based on score
        
        Args:
            current_score (int): Current game score
        
        Returns:
            bool: Whether the game should end
        """
        return current_score <= 0