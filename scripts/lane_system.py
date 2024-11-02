# Create a new file called lane_system.py in your scripts folder

class Lane:
    def __init__(self, x_position, width):
        self.x_position = x_position  # Center position of the lane
        self.width = width
        self.is_occupied = False

class LaneManager:
    def __init__(self, screen_width, num_lanes=3):
        self.screen_width = screen_width
        self.num_lanes = num_lanes
        self.lane_width = screen_width // num_lanes
        self.current_lane = 1  # Start in middle lane (0-based index)
        self.can_switch = True  # Add a flag to prevent multiple switches

    def get_lane_position(self, lane):
        return (lane * self.lane_width) + (self.lane_width // 2)

    def get_current_lane_position(self):
        return self.get_lane_position(self.current_lane)

    def switch_lane(self, direction):
        if not self.can_switch:
            return False
        
        new_lane = self.current_lane + direction
        
        # Check if new lane is valid
        if 0 <= new_lane < self.num_lanes:
            self.current_lane = new_lane
            self.can_switch = False  # Prevent switching until key is released
            return True
        return False

    def get_current_lane_position(self):
        return self.get_lane_position(self.current_lane)