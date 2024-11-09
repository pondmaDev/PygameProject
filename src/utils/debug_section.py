import datetime
import traceback
import sys

class Debug:
    def __init__(self):
        self.enabled = True
        self.sections = {
            'init': False,
            'menu': False,
            'game': False,
            'character': False,
            'items': True,
            'collision': True,
            'settings': True,
            'performance': False,
            'resources' : True
        }
        self.log_file = "game_debug.log"

    def debug_print(self, message):
        if self.enabled:
            print(f"[DEBUG] {message}")
            self.write_to_file(f"[DEBUG] {message}")

    def log(self, section, message):
        if self.enabled and self.sections.get(section, False):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] [{section.upper()}] {message}"
            print(log_message)
            self.write_to_file(log_message)

    def error(self, section, message, exc_info=False):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"[{timestamp}] [ERROR] [{section.upper()}] {message}"
        print(error_message)
        self.write_to_file(error_message)
        
        if exc_info:
            traceback_str = traceback.format_exc()
            print(traceback_str)
            self.write_to_file(traceback_str)

    def error_print(self, message):
        print(f"[ERROR] {message}")
        self.write_to_file(f"[ERROR] {message}")

    def write_to_file(self, message):
        try:
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(message + '\n')
        except Exception as e:
            print(f"Failed to write to log file: {e}")
    ##### is debug mode is use to doo loop debug #### CAREFULLY USE BEFORE YOUR GAME GONE
    def is_debug_mode(self, section=None):
        """
        Check if debug mode is enabled.
        
        Args:
            section (str, optional): Specific section to check debug mode for
        
        Returns:
            bool: Whether debug mode is enabled
        """
        if section is None:
            return self.enabled
        return self.enabled and self.sections.get(section, False)

# Create a global instance
debug = Debug()

# Add a global exception handler
def global_exception_handler(exctype, value, tb):
    debug.error('global', f"Uncaught exception: {exctype.__name__}: {value}", exc_info=True)
    # Call the default exception handler
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = global_exception_handler