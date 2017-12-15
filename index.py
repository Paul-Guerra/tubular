import platform
import logging
import config
import youtube
from show import Show
from episode import Episode
from downloader import Downloader
from uploader import Uploader
from utils.logger import initLogging

def feeds_to_shows(feeds):
  return list(map(
    lambda f: Show(f.id, f.title, get_episodes_from_entries(f)),
    feeds
  ))

def get_episodes_from_entries(feed_response):
  episodes = list(map(Episode, feed_response.entries))
  includes = list(map(
    lambda i: i.lower(),
    feed_response.manifest_item.include
    ))
  return filter(
    lambda e: title_is_included(e.title.lower(), includes),
    episodes
  )

def title_is_included(title, includes):
  for i in includes:
    if i in title:
      return True 
  return False

initLogging()
logger = logging.getLogger('tubular')

logger.info('Starting Tubular')
logger.debug('Running on Python {}'.format(platform.python_version()))
logger.debug('Log level set to {}'.format(logger.level))
config = config.load()

feeds = youtube.crawl(youtube.manifest(config))
available_shows = feeds_to_shows(feeds)
dl_manager = Downloader(available_shows)
dl_manager.run()
'''
# open_show_from_file() # creates if file does not exist
dl_manager = Downloader(available_shows, archived_shows)
new_episodes = dl_manager.run()
add new episodes to archive
rewrite archive file
'''
