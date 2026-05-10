import logging
import sys

def setup_logging():
    """Set up the logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("trading_bot.log"),
        ],
    )
    return logging.getLogger(__name__)

logger = setup_logging()
