
import random
from typing import List, Optional
from src.items.item import Item, ItemType
from src.utils.debug_section import debug

class ItemSpawner:
    """Manages spawning of items during gameplay"""
    
    def __init__(
        self, 
        screen_width: int, 
        screen_height: int, 
        num_lanes: int = 3,
        current_level: int = 1
    ):
        """
        Initialize the ItemSpawner
        
        Args:
            screen_width (int): Game screen width
            screen_height (int): Game screen height
            num_lanes (int): Number of game lanes
            current_level (int): Current game level
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_lanes = num_lanes
        self.current_level = current_level
        
        # Lane configuration
        self.lane_width = screen_width // num_lanes
        self.lane_positions = [
            (i * self.lane_width) + (self.lane_width // 2) 
            for i in range(num_lanes)
        ]
        
        # Spawn configuration
        self.max_items = 10
        self.spawn_timer = 0
        self.spawn_interval = 120
        
        # Difficulty progression
        self.difficulty_multiplier = 1.0
        
        # Level-based bad item spawn rates
        self.bad_item_spawn_rates = {
            1: 0.4,   # 20% chance of bad items in level 1
            2: 0.5,   # 30% chance of bad items in level 2
            3: 0.7,   # 40% chance of bad items in level 3
        }

    def update(self, game_speed: float, current_items: List[Item] = None) -> Optional[List[Item]]:
        """
        Update spawner and potentially spawn new items
        
        Args:
            game_speed (float): Current game speed
            current_items (List[Item], optional): Current items on screen
        
        Returns:
            Optional[List[Item]]: Newly spawned items
        """
        current_items = current_items or []
        
        # Validate game speed
        safe_game_speed = max(0.1, game_speed)
        self.minimum_fall_speed = 0
        
        # Increment spawn timer
        self.spawn_timer += 1
        
        # Check spawn conditions
        if (self.spawn_timer >= self.spawn_interval and 
            len(current_items) < self.max_items):
            
            self.spawn_timer = 0
            return self._spawn_items(safe_game_speed)
        
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
        used_lanes = set()
        
        # Randomize number of items
        num_items = random.randint(1, min(2, self.max_items))
        
        for _ in range(num_items):
            # Select an unused lane
            available_lanes = [
                lane for lane in range(self.num_lanes) 
                if lane not in used_lanes
            ]
            
            if not available_lanes:
                break
            
            lane = random.choice(available_lanes)
            used_lanes.add(lane)
            
            # Create and configure item
            new_item = self._create_item(lane)
            new_item.x = self.lane_positions[lane]
            new_item.y = 0
            
            new_items.append(new_item)
        
        return new_items

    def _create_item(self, lane: int) -> Item:
        """
        Create an item with weighted randomization based on level
        
        Args:
            lane (int): Lane for the item
        
        Returns:
            Item: Newly created item
        """
        # Get the bad item spawn rate for the current level
        bad_item_rate = self.bad_item_spawn_rates.get(
            self.current_level, 
            0.6  # Default to 60% for levels beyond defined rates
        )

        # Calculate dynamic fall speed
        base_speed = 5
        level_speed_multiplier = 1 + (self.current_level * 0.5)
        speed_variation = random.uniform(0.9, 1.1)
        fall_speed = base_speed * level_speed_multiplier * speed_variation

        # Update minimum fall speed tracking
        if self.minimum_fall_speed == 0 or fall_speed < self.minimum_fall_speed:
            self.minimum_fall_speed = fall_speed

        # Determine item type based on probability
        item_type_choice = random.random()
        if item_type_choice < bad_item_rate:
            # Spawn a bad item (red or yellow)
            if random.random() < 0.7:  # Increased chance for red item
                item_type = ItemType.BAD_RED
                fall_speed = fall_speed  # Use the calculated fall speed for the red item
            else:
                item_type = ItemType.BAD_YELLOW
                fall_speed = self.minimum_fall_speed * 10  # Set yellow item speed to 10 times the minimum speed
        elif item_type_choice < bad_item_rate + 0.05:  # Decreased chance for purple item
            item_type = ItemType.GOOD_PURPLE
        else:
            # Spawn a good item (green or blue)
            item_type = random.choice([ItemType.GOOD_GREEN, ItemType.GOOD_BLUE])
        
        return Item(
            lane=lane,
            color=item_type['color'],
            is_good=item_type['is_good'],
            size=item_type['size'],
            fall_speed=fall_speed,
            level=self.current_level
        )
            
    def get_minimum_fall_speed(self) -> float:
        """
        Get the current minimum fall speed
        
        Returns:
            float: Minimum fall speed
        """
        return self.minimum_fall_speed


    def _weighted_choice(self, item_types: List[dict]) -> dict:
        """
        Select an item type based on weighted probabilities
        
        Args:
            item_types (List[dict]): List of item types with weights
        
        Returns:
            dict: Selected item type
        """
        total_weight = sum(item['weight'] for item in item_types)
        r = random.uniform(0, total_weight)
        
        cumulative_weight = 0
        for item_type in item_types:
            cumulative_weight += item_type['weight']
            if r <= cumulative_weight:
                return item_type
        
        return item_types[0]  # Fallback