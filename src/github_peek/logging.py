from loguru import logger

from pathlib import Path

logger.remove()
logger.add(
    Path.home() / ".githubkeep.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)
