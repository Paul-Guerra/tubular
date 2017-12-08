import os
import json

app_config_path = 'config.json'

def load_config():
  if os.path.exists(app_config_path):
    print('PGD: path exists')
  else:
    raise Exception('App config not found')