import os
import json
import logging

app_config_path = '_config.json'
logger = logging.getLogger('tubular')

def load():
  try:
    if os.path.exists(app_config_path):
      with open(app_config_path, 'r') as f:
        return json.load(f)
    else:
      raise Exception('App config not found')
  except Exception as e:
    logger.critical('Error loading app config: {}'.format(str(e)))
    exit()