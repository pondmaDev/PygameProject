import random
from typing import List, Optional
from .item import Item
from src.utils.debug_section import debug

class ItemSpawner:
    def __init__(
        self, 
        screen_width: int, 
        screen_height: int, 
        num_lanes: int = 3,
        current_level: int = 1  # Add default value
    ):
        """
        Initialize the ItemSpawner
        
        Args:
            screen_width (int): Width of the game screen
            screen_height (int): Height of the game screen
            num_lanes (int): Number of lanes in the game
            current_level (int): Current game level
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_lanes = num_lanes
        
        # Add current_level as an instance attribute
        self.current_level = current_level
        
        # Calculate lane positions
        self.lane_width = screen_width // num_lanes
        self.lane_positions = [
            (i * self.lane_width) + (self.lane_width // 2) 
            for i in range(num_lanes)
        ]
        
        # Improved spawn timing variables
        self.max_items = 10  # Maximum number of items on screen
        self.spawn_timer = 0
        self.spawn_interval = 120  # Frames between spawns (adjust as needed)
        
        # Difficulty progression
        self.difficulty_multiplier = 1.0

    def update(self, game_speed: float, current_items: List[Item] = None) -> Optional[List[Item]]:
        """
        Update spawner and potentially spawn new items with robust error handling
        
        Args:
            game_speed (float): Current game speed
            current_items (List[Item], optional): Current items on screen
        
        Returns:
            Optional[List[Item]]: List of newly spawned items or None
        """
        # Use an empty list if no items are provided
        if current_items is None:
            current_items = []

        # Validate and sanitize inputs
        if game_speed <= 0:
            debug.warning('item_spawner', f"Invalid game speed: {game_speed}. Using default speed.")
            game_speed = 1.0  # Default safe speed
        
        # Increment spawn timer
        self.spawn_timer += 1
        
        try:
            # Check if enough time has passed since last spawn
            # and we haven't reached max items
            if (self.spawn_timer >= self.spawn_interval and 
                len(current_items) < self.max_items):
                
                # Reset spawn timer
                self.spawn_timer = 0
                
                # Spawn items
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
        num_items = random.randint(1, min(2, self.max_items))
        
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
        Create an item with randomized properties and adjusted size
        
        Args:
            lane (int): Lane for the item
        
        Returns:
            Item: Newly created item
        """
        # Define item colors and types with weighted probabilities
        item_types = [
            {
                'color': (0, 255, 0),  # Green (good)
                'is_good': True, 
                'weight': 3,
                'size': 40  # Slightly larger good item
            },
            {
                'color': (0, 0, 255),  # Blue (good)
                'is_good': True, 
                'weight': 3,
                'size': 40  # Medium good item
            },
            {
                'color': (255, 0, 0),  # Red (bad)
                'is_good': False, 
                'weight': 1,
                'size': 40  # Smaller bad item
            }
        ]
        
        # Weighted random selection
        total_weight = sum(item['weight'] for item in item_types)
        r = random.uniform(0, total_weight)
        
        cumulative_weight = 0
        for item_type in item_types:
            cumulative_weight += item_type['weight']
            if r <= cumulative_weight:
                # Calculate dynamic fall speed based on level
                base_speed = 5  # Base fall speed
                level_speed_multiplier = 1 + (self.current_level * 0.5)  # 50% speed increase per level
                speed_variation = random.uniform(0.9, 1.1)
                fall_speed = base_speed * level_speed_multiplier * speed_variation
                
                return Item(
                    lane=lane,
                    color=item_type['color'],
                    is_good=item_type['is_good'],
                    size=item_type['size'],
                    fall_speed=fall_speed,  # Dynamic fall speed
                    level=self.current_level
                )
        
        # Fallback
        return Item(
            lane=lane,
            color=(0, 255, 0),
            is_good=True,
            size=40,
            fall_speed=5,
            level=self.current_level
        )

    def increase_difficulty(self):
        """
        Increase game difficulty over time with more nuanced speed progression
        """
        # Increase difficulty multiplier more aggressively
        self.difficulty_multiplier *= 1.2  # 20% increase instead of 10%
        
        # Slightly increase max items, but cap it
        self.max_items = min(self.max_items + 1, 5)
        
        # Decrease spawn interval more gradually
        self.spawn_interval = max(60, int(self.spawn_interval * 0.95))