import os
from loguru import logger
from rich.console import Console
from rich.logging import RichHandler

class LoggerConfig:
    """
    A class t co configure the logger for the chatbot-emociones application.
    """

    @staticmethod
    def configure_logger(log_path: str = "./chatbot-emociones/logs", log_file: str = "app.log"):
        """
        Configures the logger to use RichHandler for better formatting and console output.
        """
        # Set the log level from environment variable or default to INFO
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        # Ensure the log directory exists
        os.makedirs(log_path, exist_ok=True)

        # Log file path
        log_file_path = os.path.join(log_path, log_file)

        # Configure the logger
        logger.remove()  # Remove the default logger
        logger.add(
            log_file_path,
            rotation="10 MB",  # Rotate log files when they reach 1 MB
            retention="7 days",  # Keep logs for 7 days
            compression="zip",  # Compress old log files
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
        )

        console = Console()
        logger.add(
           
            RichHandler(console=Console(), 
                        markup=True,
                        show_time=True, 
                        show_level=True, 
                        show_path=True),
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <bold><level>{level}</level></bold> | <cyan>{message}</cyan>",
        )

        logger.info("[cyan]Logger configured successfully.[/cyan]")

if __name__ == "__main__":
    # Example usage
    LoggerConfig.configure_logger()
    logger.info("Logger is configured and ready to use.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")