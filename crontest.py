import platform
import logging
from utils.logger import initLogging

initLogging()
logger = logging.getLogger('tubular')

logger.warning('hi from python')
logger.warning(platform.python_version())
