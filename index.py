import platform
import logging
import config
from utils.logger import initLogging
from youtube import get_user_urls

initLogging()
logger = logging.getLogger("tubular")
# print(vars(logger))
# print(logger.level)
logger.info("Starting Tubular")
logger.debug("Running on Python {}".format(platform.python_version()))
logger.debug("Log level set to {}".format(logger.level))
config = config.load()
# print(config['youtube']['url_base'])
print(get_user_urls(config))