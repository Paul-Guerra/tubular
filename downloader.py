import os
import ntpath
import logging
import youtube_dl
from utils.files import write_dict_as_json, open_json_as_dict
logger = logging.getLogger('tubular')

class Downloader(object):

  def __init__(self, subscriptions):
    self.subscriptions = subscriptions
    self._last_run_path = 'last_run.json'
    self._temp_dir = 'tmp/'
    try:
      if not os.path.exists(self._temp_dir):
        os.makedirs(self._temp_dir)
    except Exception as e:
      logger.error('Could not open {}'.format(self._temp_dir))

    try:
      if not os.path.exists(self._temp_dir):
        os.makedirs(self._temp_dir)
    except Exception as e:
      logger.exception(str(e))
      exit()

  def run(self):
    self._empty_temp_dir()    
    for show in self.subscriptions.shows:
      self._download_episodes(show)
    self._write_last_run(_ids_from_tmp_dir(self._temp_dir))
    
  @property
  def download_options(self):
    return {
      'nocheckcertificate': True,
      'keepvideo': False,
      'outtmpl': 'tmp/%(id)s.%(ext)s',
      'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
      }],
      'logger': logger,
      'progress_hooks': [_onUpdate]
    }
  
  def _write_last_run(self, ids):
    try:
      write_dict_as_json({'ids': ids}, self._last_run_path)
    except Exception as e:
      logger.error('Could not write {}'.format(self._last_run_path))
    
  def _empty_temp_dir(self):
    logger.info('Emptying {}'.format(self._temp_dir))
    try:
      fileList = os.listdir(self._temp_dir)
      for fileName in fileList:
        os.remove(self._temp_dir + '/' + fileName)
    except OSError as e:
      logger.warn('Cannot empty {}. Error: {}'.format(self._temp_dir, e))

  def _download_episodes(self, show):
    try:
      last_run_ids = set(open_json_as_dict(self._last_run_path)['ids'])
      episodes = show.get_new_episodes(last_run_ids)
      urls = list(map(lambda e: e.web_page, episodes))
      with youtube_dl.YoutubeDL(self.download_options) as ydl:
        logger.info('Initiating download for urls {}'.format(urls))
        ydl.download(urls)
      logger.info('Downloads complete')
    except Exception as e:
      logger.exception('Could not download {}: Error: {}'.format(urls, e))

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

def _onUpdate(u):
  if u['status'] is 'finished':
    logger.info('download {}: {}'.format(u['status'], u))
