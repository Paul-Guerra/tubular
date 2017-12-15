import os
import ntpath
import logging
import youtube_dl
from utils.files import write_dict_as_json, open_json_as_dict, touch
logger = logging.getLogger('tubular')

class Downloader(object):

  def __init__(self, available_shows):
    self.available_shows = available_shows
    self.__last_run_path = 'last_run.json'
    self.__temp_dir = 'tmp/'
    self.__downloaded_ids = []
    self.init_dl_tracking()
    try:
      if not os.path.exists(self.__temp_dir):
        os.makedirs(self.__temp_dir)
    except Exception as e:
      logger.exception(str(e))
      exit()

  def init_dl_tracking(self):
    default_dls = {'ids': []}
    try:
      if not os.path.exists(self.__last_run_path):
        touch(self.__last_run_path)
        write_dict_as_json(default_dls, self.__last_run_path)
      else:
        self.__downloaded_ids = open_json_as_dict(self.__last_run_path)['ids']
    except Exception as e:
      logger.exception(str(e))

  def run(self):
    self.__empty_temp_dir()
    for show in self.available_shows:
      self.__download_episodes(show)
      self.__downloaded_ids += _ids_from_tmp_dir(self.__temp_dir)
    self.__write_last_run(self.__downloaded_ids)
  
  @property
  def download_options(self):
    return {
      'simulate': True,
      'nocheckcertificate': True,
      'keepvideo': False,
      'outtmpl': '{dir}/%(id)s.%(ext)s'.format(dir=self.__temp_dir),
      'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
      }],
      'logger': logger,
      'progress_hooks': [on_download_update]
    }
  
  def __write_last_run(self, ids):
    try:
      # write_dict_as_json({'ids': ids}, self.__last_run_path)
      write_dict_as_json({'ids': []}, self.__last_run_path)
    except Exception as e:
      logger.error('Could not write {}'.format(self.__last_run_path))

  def __download_episodes(self, show):
    try:
      episodes = show.get_new_episodes(self.__downloaded_ids)
      urls = list(map(lambda e: e.web_page, episodes))
      with youtube_dl.YoutubeDL(self.download_options) as ydl:
        logger.info('Initiating download for urls {}'.format(urls))
        ydl.download(urls)
      logger.info('Downloads complete')
      self.__mark_episodes_downloaded(episodes)
      return episodes
    except Exception as e:
      logger.exception('Could not download {}: Error: {}'.format(urls, e))
    
    return []
    
  def __empty_temp_dir(self):
    logger.info('Emptying {}'.format(self.__temp_dir))
    try:
      fileList = os.listdir(self.__temp_dir)
      for fileName in fileList:
        os.remove(self.__temp_dir + '/' + fileName)
    except OSError as e:
      logger.warn('Cannot empty {}. Error: {}'.format(self.__temp_dir, e))

  def __episode_tmp_path(self, episode):
    return '{dir}/{name}.mp3'.format(dir=self.__temp_dir, name=episode.id)

  def __mark_episodes_downloaded(self, episodes):
    for e in episodes:
      e.downloaded = True
      e.tmp_path = self.__episode_tmp_path(e)

def _ids_from_tmp_dir(folder):
  try:
    file_list = os.listdir(folder)    
  except OSError as e:
    logger.warn(str(e))
    file_list = []

  return list(map(_get_id_from_path, file_list))

def _get_id_from_path(path=''):
  '''Extract the video id from the file path'''
  if type(path) is not str or path is '':
    return
  return ntpath.basename(path).split('.')[0]

def on_download_update(u):
  if u['status'] is 'finished':
    logger.info('download {}: {}'.format(u['status'], u))
