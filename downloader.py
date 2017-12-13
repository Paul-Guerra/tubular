import os
import logging
import youtube_dl
from utils.files import write_dict_as_json
logger = logging.getLogger('tubular')

class Downloader(object):

  def __init__(self, subscriptions):
    self.subscriptions = subscriptions
    self.__last_run_path = 'last_run.json'
    self.__temp_dir = 'tmp/'
    try:
      if not os.path.exists(self.__temp_dir):
        os.makedirs(self.__temp_dir)
    except Exception as e:
      logger.error('Could not open {}'.format(self.__temp_dir))
      self.__last_run = {}

    try:
      if not os.path.exists(self.__temp_dir):
        os.makedirs(self.__temp_dir)
    except Exception as e:
      logger.exception(str(e))
      exit()

  def __write_last_run(self):
    try:
      write_dict_as_json(self.__last_run, self.__last_run_path)
    except Exception as e:
      logger.error('Could not write {}'.format(self.__last_run_path))

  def run(self):
    for show in self.subscriptions.shows:
      self.__download_episodes(show)
  
  def __get_new_episodes(self, show):
    return [show.episodes[0]]

  def __download_episodes(self, show):
    
    opts = {
      'nocheckcertificate': True,
      'keepvideo': False,
      'outtmpl': 'tmp/%(id)s.%(ext)s',
      'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
      }],
      'logger': logger,
      'progress_hooks': [onUpdate]
    }

    episodes = self.__get_new_episodes(show)
    urls = list(map(lambda e: e.web_page, episodes))
    with youtube_dl.YoutubeDL(opts) as ydl:
      logger.info('Initiating download for urls {}'.format(urls))
      ydl.download(urls)

def onUpdate(u):
  logger.info('{}: {}'.format(u['status'], u))
