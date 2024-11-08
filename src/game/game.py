import pygame
import random
from src.character.character import Character
from src.ui.interface import MainMenu, LevelSelectionMenu, SettingsMenu, PauseMenu
from config.setting import current_settings
from src.game.game_state import current_game_state
from src.system.lane_system import LaneManager
from src.game.world import World
from src.utils.debug_section import debug
from src.items.items import Item
from src.utils.constant import Colors
from src.system.movement import CharacterController, move_character
from src.utils.resource_manager import ResourceManager

class Game:
    def __init__(self):
        # Add print statements to verify logging
        print("Debug initialization started")
        debug.log('init', "Debug log test - Initializing Game...")
        print("Debug log test printed")

        try:
            debug.log('init', "Attempting to initialize game variables")
            self.initialize_game_variables()
            
            debug.log('init', "Attempting to initialize pygame")
            self.initialize_pygame()
            
            debug.log('init', "Attempting to initialize game objects")
            self.initialize_game_objects()
            
            debug.log('init', "Attempting to initialize menus")
            self.initialize_menus()
            
            debug.log('init', "Attempting to initialize images")
            self.initialize_images()
            
            debug.log('init', "Attempting to initialize character")
            self.initialize_character()
            
        except Exception as e:
            print(f"Initialization error: {e}")
            debug.error('init', f"Initialization failed: {e}", exc_info=True)
            raise
        
        

    def initialize_game_variables(self):
        self.WHITE = Colors.WHITE
        self.BLACK = Colors.BLACK
        self.RED = Colors.RED
        self.GRAY = Colors.GRAY
        self.GRAY_HOVER = Colors.GRAY_HOVER
        self.game_speed = 3.0
        debug.log('init', "Game variables initialized")

    def initialize_pygame(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('CollectCat')
        debug.log('init', f"Screen dimensions set to {self.screen_width}x{self.screen_height}")

    def initialize_game_objects(self):
        self.settings = current_settings
        self.lane_manager = LaneManager(self.screen_width, num_lanes=3)
        self.character = None
        debug.log('init', "Settings and Lane manager initialized")

    def initialize_menus(self):
        try:
            debug.log('menu', "Initializing menus")
            
            # Check if screen is initialized
            if not hasattr(self, 'screen'):
                debug.error('menu', "Screen not initialized before creating menus")
                raise AttributeError("Screen must be initialized before creating menus")
            
            # Create main menu
            try:
                self.main_menu = MainMenu(self.screen)
                debug.log('menu', "Main menu initialized")
            except Exception as main_menu_error:
                debug.error('menu', f"Failed to initialize main menu: {main_menu_error}")
                raise
            
            # Create level selection menu
            try:
                self.level_menu = LevelSelectionMenu(self.screen)
                debug.log('menu', "Level selection menu initialized")
            except Exception as level_menu_error:
                debug.error('menu', f"Failed to initialize level selection menu: {level_menu_error}")
                raise
            
            # Create settings menu
            try:
                self.settings_menu = SettingsMenu(self.screen, current_settings)
                debug.log('menu', "Settings menu initialized")
            except Exception as settings_menu_error:
                debug.error('menu', f"Failed to initialize settings menu: {settings_menu_error}")
                raise
            
        except Exception as e:
            debug.error('menu', f"Menu initialization completely failed: {e}", exc_info=True)
            # You might want to handle this more gracefully, perhaps by setting default/dummy menus
            raise

    def initialize_images(self):
        self.idle_images = []
        self.running_images = []
        self.default_surface = pygame.Surface((50, 50))
        self.default_surface.fill(self.RED)
        self.idle_images = [self.default_surface]
        self.running_images = [self.default_surface]
        self.world = World(self.screen_width, self.screen_height)
        debug.log('init', "Images initialized")

    
    def initialize_reset_game_state(self):
        self.score = 0
        self.items = []
        self.item_spawner_time = 0  # This is your variable name
        debug.log('game', "Game state reset")
    
    def initialize_character(self):
        initial_x = self.lane_manager.current_lane_position  # Use the property
        self.character = Character(
            initial_x,
            self.screen_height - 100,
            50, 50,
            self.RED,
            self.idle_images,
            self.running_images
        )
        
    #HANDLE EVENT SESSION

    def handle_pause(self):
        debug.log('game', "Game paused")
        pause_menu = PauseMenu(self.screen, current_game_state.get_screen(), self.settings)
        result = pause_menu.display()
        
        if result in ['exit', 'main_menu', 'level_selection']:
            return result
        elif result == 'settings':
            return self.handle_settings_from_pause()
        return 'resume'

    def handle_settings_from_pause(self):
        debug.log('settings', "Entering settings from pause menu")
        settings_menu = SettingsMenu(self.screen, self.settings)
        settings_result = settings_menu.display()
        if settings_result == 'main_menu':
            return 'main_menu'
        elif settings_result == 'resume':
            self.apply_settings()
        return 'resume'
    
    def handle_character_movement(self):
        keys_pressed = pygame.key.get_pressed()
        if hasattr(self, 'character_controller'):
            self.character_controller.handle_input(keys_pressed)
            self.character_controller.update()

    def handle_game_logic(self):
        keys_pressed = pygame.key.get_pressed()
        move_character(self.character, keys_pressed, self.lane_manager, self.settings)
        debug.log('game', "Game logic handled")
    
    def check_collisions(self):
        if self.character:
            char_rect = pygame.Rect(self.character.x, self.character.y, self.character.width, self.character.height)
            for item in self.items[:]:  # Use a copy of the list to safely remove items
                item_rect = pygame.Rect(item.x, item.y, item.size, item.size)
                if char_rect.colliderect(item_rect):
                    new_score = self.score + item.get_points()
                    if new_score <= 0:
                        debug.log('game', f"Game over. Final score: {self.score}")
                        return self.show_game_over_screen()
                    else:
                        self.score = new_score
                        self.items.remove(item)
                    debug.log('collision', f"Collision detected! Score: {self.score}")
            
            debug.log('collision', "Collisions checked")
        return None  # Continue game if no game over

    # RENDER SESSION#
    def draw_lanes(self):
        """
        Draw visual markers for lanes (optional)
        """
        lane_width = self.screen_width // self.lane_manager.num_lanes
        for i in range(1, self.lane_manager.num_lanes):
            x = i * lane_width
            pygame.draw.line(self.screen, (200, 200, 200), 
                           (x, 0), (x, self.screen_height), 2)
        debug.log('game', "Lanes drawn")
    
    def draw_items(self):
        for item in self.items:
            item.draw(self.screen)
        debug.log('game', "Items drawn")
    
    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, self.BLACK)
        self.screen.blit(score_text, (10, 10))
        debug.log('game', f"Current score: {self.score}")
    
    def draw_game_state(self):
        self.world.draw(self.screen)
        self.draw_lanes()
        if self.character:
            self.character.update()
            self.character.draw(self.screen)
        self.draw_items()
        self.draw_score()
        debug.log('game', "Game state drawn")
    
    #Game loop SESSION
    def game_loop(self):
        clock = pygame.time.Clock()
        game_running = True

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_result = self.handle_pause()
                    if pause_result != 'resume':
                        return pause_result
                    
            self.handle_character_movement
            self.handle_game_logic()
            self.update_game_state()
            game_over_result = self.check_collisions()
            if game_over_result:
                return game_over_result

            # Draw everything
            self.screen.fill(self.WHITE)
            self.world.draw(self.screen)
            self.draw_lanes()
            if self.character:
                self.character.draw(self.screen)
            self.draw_items()
            self.draw_score()

            pygame.display.flip()
            fps = clock.get_fps()
            debug.log('performance', f"FPS: {fps:.2f}")
            clock.tick(60)

        return 'main_menu'

    
    # UPDATE GAME STATE SESSION
    def start_game(self, level):
        """
        Initialize and start the game for a specific level
        
        Args:
            level (str): The selected game level
        
        Returns:
            str: Game result ('quit', 'restart', 'main_menu', etc.)
        """
        debug.log('game', f"Starting game at level {level}")
        try:
            # Set the current game state
            current_game_state.set_screen('game')
            current_game_state.set_level(level)
            
            # Reset game state
            self.initialize_reset_game_state()
            
            # Reinitialize the character for the new game
            self.initialize_character()
            
            # Start the game loop and return its result
            return 'main_menu' # This was game_loop()
        except Exception as e:
            debug.error('game', f"Failed to start game: {e}")
            return 'main_menu'
    
    def spawn_item(self):
        lane = random.randint(0, 2)  # Random lane (0, 1, or 2)
        color = random.choice([(255, 0, 0), (0, 0, 255), (0, 255, 0)])  # Random color (red, blue, green)
        is_good = color != (255, 0, 0)  # Red items are not good
        new_item = Item(lane, color, is_good=is_good)
        self.items.append(new_item)
        debug.log('items', f"New item spawned in lane {lane} with color {color}")
    
    def show_settings(self):
        try:
            debug.log('settings', "Entering settings menu...")
            self.settings_menu = SettingsMenu(self.screen, self.settings) 
            return self.settings_menu.display()
        except Exception as e:
            debug.error('settings', f"Error showing settings: {e}")
            return 'main_menu'  # or handle accordingly
    
    def update_items(self):
        items_to_remove = []
        for item in self.items:
            item.fall()
            if item.y > self.screen_height:
                items_to_remove.append(item)
        for item in items_to_remove:
            self.items.remove(item)
        debug.log('items', "Items updated")

    def update_game_state(self):
        # Update the world (background scroll)
        self.world.update(self.game_speed)

        # Update character animation (not position)
        if self.character:
            self.character.update(self.game_speed)

        # Item spawning logic
        self.item_spawner_time += 1
        if self.item_spawner_time >= 30:
            self.spawn_item()
            self.item_spawner_time = 0

        # Update items
        for item in self.items:
            try:
                item.update(self.game_speed)
            except AttributeError as e:
                debug.error('game', f"Error updating item: {e}")
                debug.error('game', f"Item attributes: {vars(item)}")

        # Remove items that have moved off the screen
        self.items = [item for item in self.items if item.y < self.screen_height]

        debug.log('game', f"Game state updated. Speed: {self.game_speed:.2f}")
    
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
        debug.log('settings', "Settings applied")
    
    def show_game_over_screen(self):
        debug.log('game', f"Showing game over screen. Final score: {self.score}")
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Restart", True, (0, 0, 0))
        menu_text = font.render("Main Menu", True, (0, 0, 0))
        
        restart_rect = pygame.Rect(200, 300, 140, 50)
        menu_rect = pygame.Rect(460, 300, 140, 50)
        
        shadow_offset = 3
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            restart_hovered = restart_rect.collidepoint(mouse_pos)
            menu_hovered = menu_rect.collidepoint(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        return 'restart'
                    elif menu_rect.collidepoint(event.pos):
                        return 'main_menu'
            
            self.screen.fill((255, 255, 255))
            self.screen.blit(game_over_text, (400 - game_over_text.get_width() // 2, 200))
            
            # Draw shadows for hovered buttons
            if restart_hovered:
                shadow_rect = restart_rect.move(shadow_offset, shadow_offset)
                pygame.draw.rect(self.screen, (150, 150, 150), shadow_rect)
            if menu_hovered:
                shadow_rect = menu_rect.move(shadow_offset, shadow_offset)
                pygame.draw.rect(self.screen, (150, 150, 150), shadow_rect)
            
            # Draw buttons
            pygame.draw.rect(self.screen, (200, 200, 200) if not restart_hovered else (180, 180, 180), restart_rect)
            pygame.draw.rect(self.screen, (200, 200, 200) if not menu_hovered else (180, 180, 180), menu_rect)
            
            # Draw button text
            self.screen.blit(restart_text, (restart_rect.centerx - restart_text.get_width() // 2, restart_rect.centery - restart_text.get_height() // 2))
            self.screen.blit(menu_text, (menu_rect.centerx - menu_text.get_width() // 2, menu_rect.centery - menu_text.get_height() // 2))
            
            pygame.display.flip()
