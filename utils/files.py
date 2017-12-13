import os
import json
import logging

logger = logging.getLogger('tubular')

def open_json_as_dict(path=''):
  if path is '' or type(path) is not str:
    raise Exception('Bad path: "{}"'.format(path))

  if os.path.exists(path):
    with open(path, 'r') as f:
      return json.load(f)
  else:
    raise Exception('Path does not exist: "{}"'.format(path))

def write_dict_as_json(obj, path):
  with open(path, 'w') as fp:
    json.dump(obj, fp)