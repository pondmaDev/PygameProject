# debug.py
import datetime

class Debug:
    def __init__(self):
        self.enabled = False
        self.sections = {
            'init': True,
            'menu': True,
            'game': True,
            'character': True,
            'items': True,
            'collision': True,
            'settings': True,
            'performance': True
        }
        self.log_file = "game_debug.log"

    def debug_print(self, message):
        """Simple debug print for success messages"""
        if self.enabled:
            print(f"[DEBUG] {message}")
            self.write_to_file(f"[DEBUG] {message}")

    def error_print(self, message):
        """Simple error print for failure messages"""
        print(f"[ERROR] {message}")
        self.write_to_file(f"[ERROR] {message}")

    def log(self, section, message):
        """Detailed logging with sections"""
        if self.enabled and self.sections.get(section, False):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] [{section.upper()}] {message}"
            print(log_message)
            self.write_to_file(log_message)

    def write_to_file(self, message):
        with open(self.log_file, 'a') as file:
            file.write(message + '\n')

    def error(self, section, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"[{timestamp}] [ERROR] [{section.upper()}] {message}"
        print(error_message)
        self.write_to_file(error_message)

# Create a global instance
debug = Debug()