class Lane:
    def __init__(self, x_position, width):
        """Initialize a lane with a position and width."""
        self.x_position = x_position  # Center position of the lane
        self.width = width
        self.is_occupied = False

class LaneManager:
    def __init__(self, screen_width, num_lanes=3):
        """Initialize the lane manager with screen width and number of lanes."""
        self.screen_width = screen_width
        self.num_lanes = num_lanes
        self.lane_width = screen_width // num_lanes
        self.current_lane = 1  # Start in the middle lane (0-based index)
        self.can_switch = True  # Flag to prevent multiple switches
        self.lanes = [Lane(self.get_lane_position(i), self.lane_width) for i in range(num_lanes)]

    def get_lane_position(self, lane_index):
        """Calculate the center position of the lane based on its index."""
        return (lane_index * self.lane_width) + (self.lane_width // 2)

    @property
    def current_lane_position(self):
        """Return the center position of the current lane."""
        return self.get_lane_position(self.current_lane)

    def switch_lane(self, direction):
        """Switch to the adjacent lane in the specified direction."""
        if not self.can_switch:
            return False
        
        new_lane = self.current_lane + direction
        
        # Check if the new lane index is valid
        if 0 <= new_lane < self.num_lanes:
            self.current_lane = new_lane
            self.can_switch = False  # Prevent switching until key is released
            return True
        return False

    def set_can_switch(self, can_switch):
        """Set the lane switching flag."""
        self.can_switch = can_switch

    def is_lane_occupied(self, lane_index):
        """Check if the specified lane is occupied."""
        if 0 <= lane_index < self.num_lanes:
            return self.lanes[lane_index].is_occupied
        return False

    def set_lane_occupation(self, lane_index, occupied):
        """Set the occupation status of the specified lane."""
        if 0 <= lane_index < self.num_lanes:
            self.lanes[lane_index].is_occupied = occupied