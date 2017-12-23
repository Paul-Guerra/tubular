import os
import json
import logging
import ntpath

logger = logging.getLogger('tubular')

def open_json_as_dict(path=''):
    if path is '' or type(path) is not str:
        raise Exception('Bad path: "{}"'.format(path))

    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
            f.close()
    else:
        raise Exception('Path does not exist: "{}"'.format(path))

def write_dict_as_json(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f)
        f.close()

def touch(path):
    dirname = ntpath.dirname(path)
    file_name = ntpath.basename(path)
    if not os.path.exists(path):
        if len(dirname) > 0:
            os.makedirs(dirname)
            
        if len(file_name) > 0:
            open(path, 'w').close()
