import pygame
import sys
from scripts.character import Character
from scripts.movement import move_character
from scripts.interface import MainMenu, LevelSelectionMenu, PauseMenu, SettingsMenu
from scripts.setting import current_settings
from scripts.game_state import current_game_state
from scripts.lane_system import LaneManager,Lane
from scripts.items import Item
import random

class Game:
    def __init__(self):
        self.debug_print("Initializing Game...")
        try:
            pygame.init()
            # Define screen dimensions first
            self.screen_width = 800
            self.screen_height = 600
            self.debug_print(f"Screen dimensions set to {self.screen_width}x{self.screen_height}")
            
            # Create the screen
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self.debug_print("Screen created successfully")
            
            # Initialize settings and lane manager
            self.settings = current_settings
            self.debug_print("Settings initialized")
            
            self.lane_manager = LaneManager(self.screen_width, num_lanes=3)
            self.debug_print("Lane manager initialized")
            
            pygame.display.set_caption('CollectCat')
            
            # Define colors
            self.WHITE = (255, 255, 255)
            self.BLACK = (0, 0, 0)
            self.RED = (255, 0, 0)
            
            # Initialize menu classes
            self.main_menu = MainMenu(self.screen)
            self.debug_print("Main menu initialized")
            
            self.level_menu = LevelSelectionMenu(self.screen)
            self.debug_print("Level menu initialized")
            
            # Initialize image lists
            self.idle_images = []
            self.running_images = []
            
            # Create a default surface as fallback
            self.default_surface = pygame.Surface((50, 50))
            self.default_surface.fill(self.RED)
            
            # Initialize with fallback images
            self.idle_images = [self.default_surface]
            self.running_images = [self.default_surface]
            
            #initialize character by None
            self.character = None
            self.debug_print("Game initialization completed successfully")

            #initialize items fall
            self.items = []  # List to hold falling items
            self.item_spawn_timer = 0  # Timer for item spawning
            self.debug_print('Items initialization completed sucessfully')

            #score system
            self.score = 0
            self.debug_print('Score initialization completed sucessfully')
            
        except Exception as e:
            self.error_print(f"Error during game initialization: {e}")
            raise

    def debug_print(self, message):
        print(f"[DEBUG] {message}")

    def error_print(self, message):
        print(f"[ERROR] {message}")

    def load_character_images(self):
        """Load and scale character images"""
        # Clear existing images
        self.idle_images = []
        self.running_images = []
        
        # Load idle images
        for path in self.idle_image_paths:
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (50, 50))
                self.idle_images.append(image)
                self.debug_print(f"Loaded idle image: {path}")
            except Exception as e:
                self.error_print(f"Failed to load idle image {path}: {e}")
                
        # Load running images
        for path in self.running_image_paths:
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (50, 50))
                self.running_images.append(image)
                self.debug_print(f"Loaded running image: {path}")
            except Exception as e:
                self.error_print(f"Failed to load running image {path}: {e}")
                
        # If no images were loaded, create fallback images
        if not self.idle_images:
            fallback = pygame.Surface((50, 50))
            fallback.fill(self.RED)
            self.idle_images = [fallback]
            self.debug_print("Using fallback idle image")
            
        if not self.running_images:
            fallback = pygame.Surface((50, 50))
            fallback.fill(self.RED)
            self.running_images = [fallback]
            self.debug_print("Using fallback running image")


    def draw_lanes(self):
        """
        Draw visual markers for lanes (optional)
        """
        lane_width = self.screen_width // self.lane_manager.num_lanes
        for i in range(1, self.lane_manager.num_lanes):
            x = i * lane_width
            pygame.draw.line(self.screen, (200, 200, 200), 
                           (x, 0), (x, self.screen_height), 2)
    
    #items drawing session 
    def spawn_item(self):
        lane = random.randint(0, 2)  # Random lane (0, 1, or 2)
        color = random.choice([(255, 0, 0), (0, 0, 255), (0, 255, 0)])  # Random color (red, blue, green)
        new_item = Item(lane, color)
        self.items.append(new_item)
        self.debug_print(f"Spawned item at lane {lane} with color {color}")

    def update_items(self):
        for item in self.items:
            item.fall()
            if item.y > self.screen_height:  # Remove items that fall off the screen
                self.items.remove(item)

    def draw_items(self):
        for item in self.items:
            item.draw(self.screen)
    
    #Check collision between character and items
    def check_collisions(self):
        if self.character:
            char_rect = pygame.Rect(self.character.x, self.character.y, self.character.width, self.character.height)
            for item in self.items[:]:  # Use a copy of the list to safely remove items
                item_rect = pygame.Rect(item.x, item.y, item.size, item.size)
                if char_rect.colliderect(item_rect):
                    self.score += item.points
                    self.items.remove(item)
                    self.debug_print(f"Collected item. New score: {self.score}")
    
    #Interface of score
    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, self.BLACK)
        self.screen.blit(score_text, (10, 10))  # Position the score in the top-left corner
    
    #Start game session        
    def start_game(self, level):
        self.debug_print(f"Starting the game with level: {level}")
        current_game_state.set_screen('game')
        current_game_state.set_level(level)
        # You can access settings like this:
        character_speed = self.settings.character_speed
        window_mode = self.settings.window_mode
        self.score = 0

        try:
            initial_x = self.lane_manager.get_current_lane_position()
            self.character = Character(
                initial_x,
                self.screen_height - 100,
                50, 50,
                self.RED,
                self.idle_images,
                self.running_images
            )
            self.debug_print("Character initialized successfully")
        except Exception as e:
            self.error_print(f"Failed to initialize character: {e}")
            return 'main_menu'

        game_running = True
        clock = pygame.time.Clock()

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu = PauseMenu(self.screen, current_game_state.get_screen(), self.settings)
                        result = pause_menu.display()
                        
                        if result in ['exit', 'main_menu']:
                            return 'main_menu'
                        elif result == 'level_selection':
                            return 'level_selection'
                        elif result == 'settings':
                            settings_menu = SettingsMenu(self.screen, self.settings)  # Keep it simple without from_pause
                            settings_result = settings_menu.display()
                            if settings_result == 'main_menu':
                                return 'main_menu'
                            elif settings_result == 'resume':  # Add this condition
                                self.apply_settings()  # Apply any changed settings
                                continue
                        elif result == 'resume':
                            continue

            # Handle character movement
            keys_pressed = pygame.key.get_pressed()
            move_character(self.character, keys_pressed, self.lane_manager, self.settings)

            #Handle apply setting
            if keys_pressed[pygame.K_ESCAPE]:
                pause_menu = PauseMenu(self.screen, 'game', self.settings)
                result = pause_menu.display()
                if result == 'main_menu':
                    return 'main_menu'
                elif result == 'resume':
                    # Apply any changed settings here
                    self.apply_settings()
                    continue

            # Spawn items every 30 frames
            self.item_spawn_timer += 1
            if self.item_spawn_timer >= 30:  # Adjust as needed for spawn rate
                self.spawn_item()
                self.item_spawn_timer = 0

            #Check collision
            self.item_spawn_timer += 1
            if self.item_spawn_timer >= 30:
                self.spawn_item()
                self.item_spawn_timer = 0

            # Update and draw items
            self.update_items()
            self.check_collisions()

            # Draw everything
            self.screen.fill(self.WHITE)
            self.draw_lanes()
            if self.character:
                self.character.update()
                self.character.draw(self.screen)
            
            self.draw_items()
            self.draw_score()  # Draw the score on the screen

            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

        return 'main_menu'
    

    def show_settings(self):
        self.debug_print("Entering settings menu...")
        settings_menu = SettingsMenu(self.screen, self.settings)
        return settings_menu.display()
    
    def apply_settings(self):
        # Apply music volume
        pygame.mixer.music.set_volume(self.settings.bg_music_volume / 100)
        
        # Apply window mode
        if self.settings.window_mode:
            pygame.display.set_mode((self.screen_width, self.screen_height))
        else:
            pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        
        # Apply character speed
        if self.character:
            self.character.speed = self.settings.character_speed

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        current_game_state.set_screen('main_menu')
        
        while True:
            try:
                menu_option = self.main_menu.display()
                self.debug_print(f"Menu option selected: {menu_option}")
                
                if menu_option == 'start_game':
                    level = self.level_menu.display()
                    self.debug_print(f"Level selected: {level}")
                    
                    if level != 'main_menu':
                        game_result = self.start_game(level)
                        self.debug_print(f"Game result: {game_result}")
                        if game_result == 'quit':
                            break
                elif menu_option == 'settings':
                    settings_result = self.show_settings()
                    self.debug_print(f"Settings result: {settings_result}")
                    if settings_result == 'quit':
                        break
                elif menu_option == 'credits':
                    # Implement credits display here
                    pass
                elif menu_option == 'quit':
                    break
                    
            except Exception as e:
                self.error_print(f"An error occurred in the main loop: {e}")
                break

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()