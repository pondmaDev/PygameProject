# import pygame
# import pygame_gui
# import math

# class SettingsUI:
#     def __init__(self, screen_width, screen_height):
#         # Initialize Pygame GUI manager
#         self.ui_manager = pygame_gui.UIManager((screen_width, screen_height))
        
#         # Screen dimensions
#         self.screen_width = screen_width
#         self.screen_height = screen_height
        
#         # Smooth transition variables
#         self.transition_values = {}
#         self.transition_speed = 0.1
        
#         # Create UI elements
#         self._create_ui_elements()
    
#     def _create_ui_elements(self):
#         # Calculate center positioning
#         ui_width = 400
#         ui_height = 500
#         x_pos = (self.screen_width - ui_width) // 2
#         y_pos = (self.screen_height - ui_height) // 2
        
#         # Background panel for settings
#         self.settings_panel = pygame_gui.elements.UIPanel(
#             relative_rect=pygame.Rect((x_pos, y_pos), (ui_width, ui_height)),
#             starting_layer_height=1,
#             manager=self.ui_manager
#         )
        
#         # Volume Sliders with smooth transitions
#         self.bg_music_slider = self._create_smooth_slider(
#             'Background Music Volume', 
#             current_settings.bg_music_volume, 
#             (50, 100, 300, 30), 
#             0, 100
#         )
        
#         self.sound_effects_slider = self._create_smooth_slider(
#             'Sound Effects Volume', 
#             current_settings.sound_effects_volume, 
#             (50, 200, 300, 30), 
#             0, 100
#         )
        
#         # Scroll Speed Slider
#         self.scroll_speed_slider = self._create_smooth_slider(
#             'Level Scroll Speed', 
#             current_settings.level_scroll_multiplier * 100, 
#             (50, 300, 300, 30), 
#             10, 300,
#             step_size=10
#         )
        
#         # Difficulty Dropdown
#         self.difficulty_dropdown = pygame_gui.elements.UIDropDownMenu(
#             options_list=['Easy', 'Medium', 'Hard'],
#             starting_option=current_settings.difficulty.capitalize(),
#             relative_rect=pygame.Rect((50, 400, 300, 30)),
#             manager=self.ui_manager
#         )
        
#         # Apply and Reset Buttons
#         self.apply_button = pygame_gui.elements.UIButton(
#             relative_rect=pygame.Rect((100, 450, 100, 40)),
#             text='Apply',
#             manager=self.ui_manager
#         )
        
#         self.reset_button = pygame_gui.elements.UIButton(
#             relative_rect=pygame.Rect((250, 450, 100, 40)),
#             text='Reset',
#             manager=self.ui_manager
#         )
    
#     def _create_smooth_slider(self, label, current_value, rect, min_val, max_val, step_size=1):
#         """Create a slider with smooth value transition"""
#         # Store initial transition value
#         self.transition_values[label] = {
#             'current': current_value,
#             'target': current_value
#         }
        
#         # Create slider
#         slider = pygame_gui.elements.UIHorizontalSlider(
#             relative_rect=pygame.Rect(rect),
#             start_value=current_value,
#             value_range=(min_val, max_val),
#             manager=self.ui_manager
#         )
        
#         return slider
    
#     def update(self, time_delta):
#         """Update UI and handle smooth transitions"""
#         # Update UI manager
#         self.ui_manager.update(time_delta)
        
#         # Handle smooth value transitions
#         self._handle_smooth_transitions()
    
#     def _handle_smooth_transitions(self):
#         """Smoothly interpolate slider values"""
#         for label, transition in self.transition_values.items():
#             # Smooth transition using lerp (linear interpolation)
#             transition['current'] = self._lerp(
#                 transition['current'], 
#                 transition['target'], 
#                 self.transition_speed
#             )
    
#     def _lerp(self, start, end, alpha):
#         """Linear interpolation for smooth transitions"""
#         return start + alpha * (end - start)
    
#     def handle_events(self, event):
#         """Handle UI events"""
#         if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
#             if event.ui_element == self.bg_music_slider:
#                 # Update transition target
#                 self.transition_values['Background Music Volume']['target'] = event.value
#                 current_settings.bg_music_volume = int(event.value)
            
#             elif event.ui_element == self.sound_effects_slider:
#                 self.transition_values['Sound Effects Volume']['target'] = event.value
#                 current_settings.sound_effects_volume = int(event.value)
            
#             elif event.ui_element == self.scroll_speed_slider:
#                 # Convert slider value to multiplier
#                 multiplier = event.value / 100
#                 self.transition_values['Level Scroll Speed']['target'] = event.value
#                 current_settings.set_level_scroll_multiplier(multiplier)
        
#         elif event.type == pygame_gui.UI_BUTTON_PRESSED:
#             if event.ui_element == self.apply_button:
#                 self._apply_settings()
#             elif event.ui_element == self.reset_button:
#                 self._reset_settings()
        
#         # Pass events to UI manager
#         self.ui_manager.process_events(event)
    
#     def _apply_settings(self):
#         """Apply current settings"""
#         # Save settings to file
#         current_settings.save_settings()
        
#         # Optional: Add visual feedback (e.g., brief notification)
#         print("Settings applied successfully!")
    
#     def _reset_settings(self):
#         """Reset settings to defaults"""
#         current_settings.reset_to_defaults()
        
#         # Reset UI elements to default values
#         self.bg_music_slider.set_current_value(50)
#         self.sound_effects_slider.set_current_value(50)
#         self.scroll_speed_slider.set_current_value(100)
#         self.difficulty_dropdown.selected_option = 'Medium'
    
#     def draw(self, screen):
#         """Draw UI elements"""
#         # Draw UI manager
#         self.ui_manager.draw_ui(screen)

# # Usage in main game loop
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
    
#     settings_ui = SettingsUI(screen.get_width(), screen.get_height())
    
#     clock = pygame.time.Clock()
#     running = True
    
#     while running:
#         time_delta = clock.tick(60)/1000.0
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
            
#             # Handle settings UI events
#             settings_ui.handle_events(event)
        
#         # Update settings UI
#         settings_ui.update(time_delta)
        
#         # Clear screen
#         screen.fill((30, 30, 30))  # Dark background
        
#         # Draw settings UI
#         settings_ui.draw(screen)
        
#         pygame.display.update()
    
#     pygame.quit()

# if __name__ == "__main__":
#     main()