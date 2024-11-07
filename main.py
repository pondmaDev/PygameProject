import pygame
import sys
import random
from scripts.character import Character
from scripts.movement import move_character
from scripts.interface import MainMenu, LevelSelectionMenu, PauseMenu, SettingsMenu
from scripts.setting import current_settings
from scripts.game_state import current_game_state
from scripts.lane_system import LaneManager, Lane
from scripts.items import Item
from scripts.world import World
from debug import debug

class Game:
    def __init__(self):
        debug.log('init', "Initializing Game...")
        self.initialize_game_variables()
        self.initialize_pygame()
        self.initialize_game_objects()
        self.initialize_menus()
        self.initialize_images()

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
        self.main_menu = MainMenu(self.screen)
        self.level_menu = LevelSelectionMenu(self.screen)
        debug.log('init', "Menus initialized")

    def initialize_images(self):
        self.idle_images = []
        self.running_images = []
        self.default_surface = pygame.Surface((50, 50))
        self.default_surface.fill(self.RED)
        self.idle_images = [self.default_surface]
        self.running_images = [self.default_surface]
        self.world = World(self.screen_width, self.screen_height)
        debug.log('init', "Images initialized")

    def initialize_game_variables(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.game_speed = 6.0
        debug.log('init', "Game variables initialized")
    
    def initialize_reset_game_state(self):
        self.score = 0
        self.items = []
        self.item_spawner_time = 0  # This is your variable name
        debug.log('game', "Game state reset")

    def load_character_images(self):
        """Load and scale character images"""
        debug.log('character', "Starting to load character images")
        
        # Clear existing images
        self.idle_images = []
        self.running_images = []
        
        # Load idle images
        for path in self.idle_image_paths:
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (50, 50))
                self.idle_images.append(image)
                debug.debug_print(f"Loaded idle image: {path}")
                debug.log('character', f"Loaded idle image: {path}")
            except Exception as e:
                debug.error_print(f"Failed to load idle image {path}: {e}")
                debug.error('character', f"Failed to load idle image {path}: {e}")
                
        # Load running images
        for path in self.running_image_paths:
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (50, 50))
                self.running_images.append(image)
                debug.debug_print(f"Loaded running image: {path}")
                debug.log('character', f"Loaded running image: {path}")
            except Exception as e:
                debug.error_print(f"Failed to load running image {path}: {e}")
                debug.error('character', f"Failed to load running image {path}: {e}")
                
        # If no images were loaded, create fallback images
        if not self.idle_images:
            fallback = pygame.Surface((50, 50))
            fallback.fill(self.RED)
            self.idle_images = [fallback]
            debug.debug_print("Using fallback idle image")
            debug.log('character', "Using fallback idle image")
            
        if not self.running_images:
            fallback = pygame.Surface((50, 50))
            fallback.fill(self.RED)
            self.running_images = [fallback]
            debug.debug_print("Using fallback running image")
            debug.log('character', "Using fallback running image")
        
        debug.log('character', "Character images loading completed")

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

    def spawn_item(self):
        lane = random.randint(0, 2)  # Random lane (0, 1, or 2)
        color = random.choice([(255, 0, 0), (0, 0, 255), (0, 255, 0)])  # Random color (red, blue, green)
        is_good = color != (255, 0, 0)  # Red items are not good
        new_item = Item(lane, color, is_good=is_good)
        self.items.append(new_item)
        debug.log('items', f"New item spawned in lane {lane} with color {color}")

    def update_items(self):
        for item in self.items:
            item.fall()
            if item.y > self.screen_height:  # Remove items that fall off the screen
                self.items.remove(item)
        debug.log('items', "Items updated")

    def draw_items(self):
        for item in self.items:
            item.draw(self.screen)
        debug.log('game', "Items drawn")

    def initialize_character(self):
        initial_x = self.lane_manager.get_current_lane_position()
        self.character = Character(
            initial_x,
            self.screen_height - 100,
            50, 50,
            self.RED,
            self.idle_images,
            self.running_images
        )
        debug.log('character', "Character initialized successfully")

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

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, self.BLACK)
        self.screen.blit(score_text, (10, 10))
        debug.log('game', f"Current score: {self.score}")

    def start_game(self, level):
        debug.log('game', f"Starting the game with level: {level}")
        current_game_state.set_screen('game')
        current_game_state.set_level(level)
        self.initialize_reset_game_state()  

        try:
            self.initialize_character()
        except Exception as e:
            debug.error('game', f"Failed to initialize character: {e}")
            return 'main_menu'

        return self.game_loop()

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

    def handle_game_logic(self):
        keys_pressed = pygame.key.get_pressed()
        move_character(self.character, keys_pressed, self.lane_manager, self.settings)
        debug.log('game', "Game logic handled")
    

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

    def draw_game_state(self):
        self.world.draw(self.screen)
        self.draw_lanes()
        if self.character:
            self.character.update()
            self.character.draw(self.screen)
        self.draw_items()
        self.draw_score()
        debug.log('game', "Game state drawn")

    def show_settings(self):
        debug.log('settings', "Entering settings menu...")
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
        debug.log('settings', "Settings applied")

    def run(self):
        current_game_state.set_screen('main_menu')
        
        while True:
            try:
                menu_option = self.main_menu.display()
                debug.debug_print(f"Menu option selected: {menu_option}")
                
                if menu_option == 'start_game':
                    while True:  # Add this loop to handle restarts
                        level = self.level_menu.display()
                        debug.debug_print(f"Level selected: {level}")
                        if level != 'main_menu':
                            self.initialize_reset_game_state()  # Reset game state before starting
                            game_result = self.start_game(level)
                            debug.debug_print(f"Game result: {game_result}")
                            if game_result == 'quit':
                                return
                            elif game_result == 'restart':
                                continue  # This will restart the game with the same level
                            elif game_result == 'main_menu':
                                break  # Break the inner loop to return to main menu
                        else:
                            break
                elif menu_option == 'settings':
                    settings_result = self.show_settings()
                    debug.debug_print(f"Settings result: {settings_result}")
                    if settings_result == 'quit':
                        break
                elif menu_option == 'credits':
                    # Implement credits display here
                    pass
                elif menu_option == 'quit':
                    break
                    
            except Exception as e:
                debug.error_print(f"An error occurred in the main loop: {e}")  # Use debug.error_print
                debug.error('game', f"An error occurred in the main loop: {e}")  # Log the error
                break

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()