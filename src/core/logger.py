from loguru import logger
import sys

# Configure logger to save to a file and output to terminal
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/system.log", rotation="10 MB", level="DEBUG")