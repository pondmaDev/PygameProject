import datetime
import traceback
import sys
import os
import logging
from typing import Optional, Dict, Union

class DebugLogger:
    """
    Advanced debugging and logging utility with granular control
    """
    
    def __init__(self, 
                 log_file: Optional[str] = None, 
                 enabled: bool = True, 
                 log_level: int = logging.DEBUG):
        """
        Initialize the debug logger with configurable settings
        
        Args:
            log_file (str, optional): Path to the log file
            enabled (bool): Global debug mode toggle
            log_level (int): Logging level from logging module
        """
        self.enabled = enabled
        
        # Set default log file path if not provided
        if log_file is None:
            # Use project root directory or a default logs folder
            project_root = self._find_project_root()
            logs_dir = os.path.join(project_root, 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            log_file = os.path.join(logs_dir, 'game_debug.log')
        
        self.log_file = log_file
        
        # Configurable debug sections with more flexibility
        self.sections: Dict[str, bool] = {
            'init': False,
            'menu': False,
            'game': False,
            'character': False,
            'items': False,
            'collision': False,
            'settings': False,
            'performance': False,
            'resources': False
        }
        
        # Configure logging
        self._configure_logging(log_level)
    
    def _find_project_root(self) -> str:
        """
        Find the root directory of the project
        
        Returns:
            str: Path to the project root
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up multiple levels to find a suitable root
        for _ in range(3):  # Adjust this if needed
            parent_dir = os.path.dirname(current_dir)
            if os.path.exists(os.path.join(parent_dir, 'main.py')):
                return parent_dir
            current_dir = parent_dir
        
        # Fallback to a default logs directory in the user's home directory
        return os.path.join(os.path.expanduser('~'), 'PygameProjectLogs')


    def _configure_logging(self, log_level: int):
        """
        Configure logging with file and console handlers
        
        Args:
            log_level (int): Logging level
        """
        # Ensure log directory exists
        log_dir = os.path.dirname(self.log_file)
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        
        # Add file handler to root logger
        logging.getLogger().addHandler(file_handler)

    def debug_print(self, message: str):
        """
        Print debug message if debug is enabled
        
        Args:
            message (str): Debug message to print
        """
        if self.enabled:
            logging.debug(message)

    def log(self, section: str, message: str):
        """
        Log message for a specific section
        
        Args:
            section (str): Debug section
            message (str): Log message
        """
        if self.enabled and self.sections.get(section, False):
            logging.info(f"[{section.upper()}] {message}")

    def error(self, 
              section: str, 
              message: str, 
              exc_info: Union[bool, Exception] = False):
        """
        Log an error with optional exception details
        
        Args:
            section (str): Error section
            message (str): Error message
            exc_info (bool or Exception): Exception information
        """
        # Log the error message
        logging.error(f"[{section.upper()}] {message}")
        
        # Handle exception traceback
        if exc_info:
            if isinstance(exc_info, bool) and exc_info:
                logging.error(traceback.format_exc())
            elif isinstance(exc_info, Exception):
                logging.error(traceback.format_exc())

    def error_print(self, message: str):
        """
        Print and log an error message
        
        Args:
            message (str): Error message
        """
        logging.error(message)

    def is_debug_mode(self, section: Optional[str] = None) -> bool:
        """
        Check if debug mode is enabled for a specific section or globally
        
        Args:
            section (str, optional): Specific section to check
        
        Returns:
            bool: Debug mode status
        """
        if section is None:
            return self.enabled
        return self.enabled and self.sections.get(section, False)

    def set_section_debug(self, section: str, enabled: bool):
        """
        Dynamically enable or disable debug for a specific section
        
        Args:
            section (str): Debug section to modify
            enabled (bool): Enable or disable debug
        """
        if section in self.sections:
            self.sections[section] = enabled
        else:
            logging.warning(f"Section {section} not found in debug sections")

# Create a global instance
debug = DebugLogger()

def global_exception_handler(exctype, value, tb):
    """
    Global exception handler for unhandled exceptions
    
    Args:
        exctype (type): Exception type
        value (Exception): Exception instance
        tb (traceback): Traceback object
    """
    debug.error(
        'global', 
        f"Uncaught exception: {exctype.__name__}: {value}", 
        exc_info=True
    )
    # Call the default exception handler
    sys.__excepthook__(exctype, value, tb)

# Set the global exception handler
sys.excepthook = global_exception_handler