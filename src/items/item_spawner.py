import random
from typing import List, Optional
from .item import Item
from src.utils.debug_section import debug

class ItemSpawner:
    def __init__(
        self, 
        screen_width: int, 
        screen_height: int, 
        num_lanes: int = 3
    ):
        """
        Initialize the ItemSpawner
        
        Args:
            screen_width (int): Width of the game screen
            screen_height (int): Height of the game screen
            num_lanes (int): Number of lanes in the game
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_lanes = num_lanes
        # Calculate lane positions
        self.lane_width = screen_width // num_lanes
        self.lane_positions = [
            (i * self.lane_width) + (self.lane_width // 2) 
            for i in range(num_lanes)
        ]
        
         # Spawn timing variables #### ADJUST SPAWN RATE
        self.max_items = 1
        self.spawn_timer = 3
        self.spawn_interval = 4.0  # Spawn every 2 seconds
        self.min_spawn_interval = 0.5  # Minimum time between spawns
        self.max_spawn_interval = 3.0  # Maximum time between spawns
        
        # Difficulty progression
        self.difficulty_multiplier = 1.0

    def update(self, game_speed: float) -> Optional[List[Item]]:
        """
        Update spawner and potentially spawn new items with robust error handling
        
        Args:
            game_speed (float): Current game speed
        
        Returns:
            Optional[List[Item]]: List of newly spawned items or None
        """
        # Validate and sanitize inputs
        if game_speed <= 0:
            debug.warning('item_spawner', f"Invalid game speed: {game_speed}. Using default speed.")
            game_speed = 1.0  # Default safe speed
        
        # Increment spawn timer
        self.spawn_timer += 1
        
        try:
            # Prevent division by zero and handle extreme values
            difficulty_factor = max(0.1, self.difficulty_multiplier)
            adjusted_interval = max(
                10, 
                int(self.spawn_interval / (game_speed * difficulty_factor))
            )
            
            # Check if it's time to spawn items
            if self.spawn_timer >= adjusted_interval:
                self.spawn_timer = 0
                return self._spawn_items(game_speed)
            
            return None
        
        except Exception as e:
            debug.error('item_spawner', f"Error in item spawner update: {e}")
            return None

    def _spawn_items(self, game_speed: float) -> List[Item]:
        """
        Spawn items with randomized properties
        
        Args:
            game_speed (float): Current game speed
        
        Returns:
            List[Item]: Newly spawned items
        """
        new_items = []
        
        # Randomize number of items to spawn
        num_items = random.randint(1, min(3, self.max_items))
        
        # Keep track of used lanes to avoid spawning multiple items in same lane
        used_lanes = set()
        
        for _ in range(num_items):
            # Select an unused lane
            available_lanes = [
                lane for lane in range(self.num_lanes) 
                if lane not in used_lanes
            ]
            
            if not available_lanes:
                break
            
            # Choose a lane
            lane = random.choice(available_lanes)
            used_lanes.add(lane)
            
            # Create item
            new_item = self._create_item(lane)
            
            # Set item position
            new_item.x = self.lane_positions[lane]
            new_item.y = 0  # Start from top of screen
            
            new_items.append(new_item)
        
        return new_items

    def _create_item(self, lane: int) -> Item:
        """
        Create an item with randomized properties
        
        Args:
            lane (int): Lane for the item
        
        Returns:
            Item: Newly created item
        """
        # Define item colors and types
        item_types = [
            {'color': (255, 0, 0), 'is_good': False},    # Red (bad)
            {'color': (0, 255, 0), 'is_good': True},     # Green (good)
            {'color': (0, 0, 255), 'is_good': True},     # Blue (good)
            {'color': (255, 255, 0), 'is_good': True},   # Yellow (good)
        ]
        
        # Randomly select item type
        item_type = random.choice(item_types)
        
        return Item(
            lane=lane,
            color=item_type['color'],
            is_good=item_type['is_good']
        )

    def increase_difficulty(self):
        """
        Increase game difficulty over time
        """
        self.difficulty_multiplier *= 1.1  # Increase difficulty by 10%
        self.max_items += 1  # Allow more items on screen