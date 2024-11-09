import pygame
import random
from src.character.character import Character
from src.character.character_controller import CharacterController
from src.ui.interface import MainMenu, LevelSelectionMenu, SettingsMenu, PauseMenu
from config.setting import current_settings
from src.game.game_state import current_game_state
from src.system.lane_system import LaneManager
from src.game.world import World
from src.utils.debug_section import debug
from src.items import Item, ItemSpawner
from src.utils.constant import Colors
from src.system.movement import move_character
from src.utils.resource_manager import ResourceManager
from src.system.collision import CollisionManager

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
        self.item_spawner = ItemSpawner(
            screen_width=self.screen_width, 
            screen_height=self.screen_height,
            num_lanes=self.lane_manager.num_lanes  # Assuming you have a lane manager
        )
        # Initialize items list
        self.items = []
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
        self.score = 10
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
    def handle_input(self, keys_pressed):
        """
        Handle lane switching based on key presses.
        
        Args:
            keys_pressed: Pygame key state dictionary
        """
        if not (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT]):
            self.lane_manager.can_switch = True  # Reset the switch flag when keys are released
        
        if keys_pressed[pygame.K_LEFT] and self.lane_manager.can_switch:
            if self.lane_manager.switch_lane(-1):
                self.character.is_switching_lanes = True
                self.character.target_x = self.lane_manager.current_lane_position
        
        elif keys_pressed[pygame.K_RIGHT] and self.lane_manager.can_switch:
            if self.lane_manager.switch_lane(1):
                self.character.is_switching_lanes = True
                self.character.target_x = self.lane_manager.current_lane_position

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
    
    # In game.py, modify the check_collisions method
    def check_collisions(self):
        collision_results = CollisionManager.check_item_collisions(
            self.character, 
            self.items
        )
        
        if collision_results:
            # Update score
            new_score = self.score + collision_results['score_change']
            
            # Remove collected items
            for item in collision_results['items_to_remove']:
                self.items.remove(item)
            
            # Check for game over
            if CollisionManager.is_game_over(new_score):
                debug.log('game', f"Game over. Final score: {new_score}")
                return self.show_game_over_screen()
            
            # Update score if not game over
            self.score = new_score
        
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
        debug.log('game', "GAME LOOP: Entering game loop")
        try:
            clock = pygame.time.Clock()
            game_running = True
            frame_count = 0
            
            # Initialize last time for delta time calculation
            last_time = pygame.time.get_ticks()

            while game_running:
                frame_count += 1
                
                # Calculate delta time
                current_time = pygame.time.get_ticks()
                dt = (current_time - last_time) / 1000.0  # Convert to seconds
                last_time = current_time
                
                # Extensive logging for each frame
                if frame_count % 60 == 0:  # Log every 60 frames
                    debug.log('game', f"GAME LOOP: Frame {frame_count}, Current state tracking")

                # Event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        debug.log('game', "GAME LOOP: Quit event detected")
                        return 'quit'
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        debug.log('game', "GAME LOOP: Pause event detected")
                        pause_result = self.handle_pause()
                        debug.log('game', f"GAME LOOP: Pause result - {pause_result}")
                        
                        if pause_result != 'resume':
                            return pause_result
                    
                    # Additional event handling if needed
                
                # Get current key states
                keys_pressed = pygame.key.get_pressed()
                
                # Game logic
                try:
                    # Handle character movement with delta time
                    # Use character_controller instead of character.controller
                    if hasattr(self, 'character_controller'):
                        self.character_controller.handle_input(keys_pressed)
                        self.character_controller.update(dt)
                    
                    # Other game logic updates
                    self.handle_game_logic()
                    self.update_game_state(dt)  # Pass dt to update_game_state
                    
                    # Collision check with detailed logging
                    game_over_result = self.check_collisions()
                    if game_over_result:
                        debug.log('game', f"GAME LOOP: Game over result - {game_over_result}")
                        return game_over_result

                    # Rendering
                    self.screen.fill(self.WHITE)
                    self.world.draw(self.screen)
                    self.draw_lanes()
                    if self.character:
                        self.character.draw(self.screen)
                    self.draw_items()
                    self.draw_score()

                    pygame.display.flip()
                    
                    # Performance monitoring
                    fps = clock.get_fps()
                    debug.log('performance', f"FPS: {fps:.2f}")
                    clock.tick(60)

                except Exception as logic_error:
                    debug.error('game', f"GAME LOOP LOGIC ERROR: {logic_error}")
                    import traceback
                    debug.error('game', f"Full traceback: {traceback.format_exc()}")
                    # Return to main menu on critical error
                    return 'main_menu'

            debug.log('game', "GAME LOOP: Exited main game loop, returning to main menu")
            return 'main_menu'

        except Exception as e:
            debug.error('game', f"GAME LOOP CRITICAL ERROR: {e}")
            import traceback
            debug.error('game', f"Full traceback: {traceback.format_exc()}")
            return 'main_menu'

    
    # UPDATE GAME STATE SESSION
    def start_game(self, level):
        """
        Initialize and start the game for a specific level
        
        Args:
            level (int or str): The selected game level
        
        Returns:
            str: Game result ('quit', 'restart', 'main_menu', 'level_selection')
        """
        debug.log('game', f"START GAME: Attempting to start level {level}")
        try:
            # Ensure level is converted to an integer
            level = int(level)
            
            # Set the current game state
            current_game_state.set_screen('game')
            current_game_state.set_level(level)
            
            # Reset game state
            self.initialize_reset_game_state()
            
            # Reinitialize the character for the new game
            self.initialize_character()
            
            # Create character controller
            self.character_controller = CharacterController(
                self.character, 
                self.lane_manager, 
                self.settings
            )
            
            # Actual game loop
            result = self.game_loop()
            
            # Log the result with full tracing
            debug.log('game', f"START GAME: Game loop completed with result: {result}")
            
            # Ensure a valid result is returned
            if result not in ['quit', 'restart', 'main_menu', 'level_selection']:
                debug.warning('game', f"UNEXPECTED RESULT: Game loop returned unexpected result: {result}")
                
                # Add stack trace for unexpected result
                import traceback
                debug.warning('game', f"Traceback: {traceback.format_stack()}")
                
                return 'main_menu'
            
            return result
        
        except Exception as e:
            # Log full exception details
            debug.error('game', f"GAME START ERROR: {e}")
            import traceback
            debug.error('game', f"Full traceback: {traceback.format_exc()}")
            return 'main_menu'
        
    def spawn_item(self):
        lane = random.randint(0, 2)  # Random lane (0, 1, or 2)
        color = random.choice([(255, 0, 0), (0, 0, 255), (0, 255, 0)])  # Random color (red, blue, green)
        is_good = color != (255, 0, 0)  # Red items are not good
        new_item = Item(lane, color, is_good=is_good)
        self.items.append(new_item)
        debug.log('items', f"New item spawned in lane {lane} with color {color}")
    
    def show_settings(self):
        """
        Display the settings menu with comprehensive error handling
        
        Returns:
            str: Result of settings menu interaction 
                ('main_menu', 'quit', or other specific states)
        """
        try:
            # Log entry into settings
            debug.log('settings', "Entering settings menu...")
            
            # Validate screen and settings before creating menu
            if not hasattr(self, 'screen') or self.screen is None:
                debug.error('settings', "Invalid screen object")
                return 'main_menu'
            
            if not hasattr(self, 'settings') or self.settings is None:
                debug.error('settings', "Invalid settings object")
                return 'main_menu'
            
            # Create settings menu with error checking
            try:
                self.settings_menu = SettingsMenu(self.screen, self.settings)
            except Exception as menu_init_error:
                debug.error('settings', f"Failed to initialize settings menu: {menu_init_error}")
                return 'main_menu'
            
            # Display settings menu with additional error handling
            try:
                settings_result = self.settings_menu.display()
                
                # Log the result of settings interaction
                debug.log('settings', f"Settings menu result: {settings_result}")
                
                # Validate and sanitize the result
                if settings_result is None:
                    debug.warning('settings', "Settings menu returned None, defaulting to main_menu")
                    return 'main_menu'
                
                return settings_result
            
            except Exception as display_error:
                debug.error('settings', f"Error displaying settings menu: {display_error}")
                return 'main_menu'
        
        except Exception as unexpected_error:
            # Catch any unexpected errors
            debug.error('settings', f"Unexpected error in show_settings: {unexpected_error}")
            return 'main_menu'
    
    def update_items(self):
        items_to_remove = []
        for item in self.items:
            item.fall()
            if item.y > self.screen_height:
                items_to_remove.append(item)
        for item in items_to_remove:
            self.items.remove(item)
        debug.log('items', "Items updated")

    def update_game_state(self, dt):
        # Update the world (background scroll)
        self.world.update(self.game_speed * dt)

        # Update character animation
        try:
            if hasattr(self, 'character_controller'):
                self.character_controller.update(self.game_speed * dt)
        except Exception as e:
            debug.error('game', f"Error updating character controller: {e}")

        # Spawn items
        try:
            # Let the item spawner determine when to spawn items
            new_items = self.item_spawner.update(self.game_speed * dt)
            
            # Add any newly spawned items to the game items list
            if new_items:
                self.items.extend(new_items)
        except Exception as e:
            debug.error('item_spawner', f"Error in item spawning: {e}")

        # Update items and remove off-screen items
        self.items = [
            item for item in self.items 
            if item.update(self.game_speed * dt, self.screen_height)
        ]

        debug.log('game', f"Game state updated. Speed: {self.game_speed:.2f}")

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
