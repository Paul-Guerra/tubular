import platform
import logging
import config
import youtube
from subscriptions import Subscriptions
from downloader import Downloader
from utils.logger import initLogging

initLogging()
logger = logging.getLogger('tubular')
# print(vars(logger))
# print(logger.level)
logger.info('Starting Tubular')
logger.debug('Running on Python {}'.format(platform.python_version()))
logger.debug('Log level set to {}'.format(logger.level))
config = config.load()
feeds = youtube.crawl(youtube.manifest(config))
subscriptions = Subscriptions(feeds)
dl_manager = Downloader(subscriptions)

# print(config['youtube']['url_base'])
print(subscriptions)
print(dl_manager)