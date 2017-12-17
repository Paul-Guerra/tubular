import platform
import logging
import config
import youtube
from show import (
  Show,
  feeds_to_shows,
  open_show_from_file, 
  get_archived_shows
  )
from episode import Episode, parse_entry
from downloader import Downloader
from uploader import Uploader
from utils.logger import initLogging
import utils.files as uf

initLogging()
logger = logging.getLogger('tubular')

uf.touch('data/')

logger.info('Starting Tubular')
logger.debug('Running on Python {}'.format(platform.python_version()))
logger.debug('Log level set to {}'.format(logger.level))
config = config.load()

feeds = youtube.crawl(youtube.manifest(config))
available_shows = feeds_to_shows(feeds)
# archived_shows = get_archived_shows()
dl_manager = Downloader(available_shows)
dl_manager.run()

# open_show_from_file('data/')
'''
# open_show_from_file() # creates default if file does not exist
dl_manager = Downloader(available_shows, archived_shows)
new_episodes = dl_manager.run()
add new episodes to archive
rewrite archive file
'''
