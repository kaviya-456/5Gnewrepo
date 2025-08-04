import logging
import os
from datetime import datetime
from config.config import config

def setup_logging(log_level: str = "INFO", log_to_file: bool = True):
    """Setup logging configuration for the framework"""
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if enabled)
    if log_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"test_run_{timestamp}.log"
        log_filepath = os.path.join(config.report.logs_dir, log_filename)
        
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.DEBUG)  # File gets all messages
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logging.info(f"Logging to file: {log_filepath}")
    
    return logger

# Initialize logging when module is imported
logger = setup_logging()