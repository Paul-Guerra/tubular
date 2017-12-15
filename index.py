import platform
import logging
import config
import youtube
# from subscriptions import Subscriptions
from show import Show
from episode import Episode
from downloader import Downloader
from uploader import Uploader
from utils.logger import initLogging

def feeds_to_shows(feeds):
  return list(map(lambda f: Show(f.id, f.title, get_episodes(f)), feeds))

def get_episodes(response):
  return list(map(Episode, response.entries))

initLogging()
logger = logging.getLogger('tubular')
# print(vars(logger))
# print(logger.level)
logger.info('Starting Tubular')
logger.debug('Running on Python {}'.format(platform.python_version()))
logger.debug('Log level set to {}'.format(logger.level))
config = config.load()
feeds = youtube.crawl(youtube.manifest(config))
# subscriptions = Subscriptions(feeds)
available_shows = feeds_to_shows(feeds)
dl_manager = Downloader(available_shows)
dl_manager.run()
# print(config['youtube']['url_base'])
# print(subscriptions)
# print(dl_manager)
