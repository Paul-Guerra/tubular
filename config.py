import os
import json
import logging
from utils.files import open_json_as_dict
logger = logging.getLogger('tubular')

def load():
  try:
    return open_json_as_dict('config.json')
  except Exception as e:
    logger.critical('Error loading app config: {}'.format(str(e)))
    exit()

