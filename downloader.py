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
      logger.warn('Could not open {}'.format(self.__temp_dir))
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
      logger.warn('Could not write {}'.format(self.__last_run_path))

  def run(self):
    for show in self.subscriptions:
      self.download_episodes(show)
  
  # def __download_episodes(self, show):
    # for episode in show.episodes:
      

