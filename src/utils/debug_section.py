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
                 enabled: bool = True, 
                 log_level: int = logging.DEBUG):
        """
        Initialize the debug logger with configurable settings
        
        Args:
            enabled (bool): Global debug mode toggle
            log_level (int): Logging level from logging module
        """
        self.enabled = enabled
        
        # Configurable debug sections with more flexibility
        self.sections: Dict[str, bool] = {
            'init': False,
            'menu': True,
            'game': False,
            'character': False,
            'items': True,
            'collision': True,
            'settings': True,
            'performance': False,
            'resources': True
        }
        
        # Configure logging
        self._configure_logging(log_level)
    
    def _configure_logging(self, log_level: int):
        """
        Configure logging with console handler only
        
        Args:
            log_level (int): Logging level
        """
        # Configure logging to output to console only
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

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

    def warning(self, section: str, message: str):
        """
        Log a warning message for a specific section
        
        Args:
            section (str): Debug section
            message (str): Warning message
        """
        if self.enabled and self.sections.get(section, False):
            logging.warning(f"[{section.upper()}] {message}")

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