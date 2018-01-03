import os
import json
import logging
import ntpath

logger = logging.getLogger('tubular')

def open_json_as_dict(path=''):
    '''Opens a JSON file and converts it to a dictionary'''
    if path is '' or type(path) is not str:
        raise Exception('Bad path: "{}"'.format(path))

    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
            f.close()
    else:
        raise Exception('Path does not exist: "{}"'.format(path))

def write_dict_as_json(obj, path):
    '''Convert a dictionary to JSON and write to path'''
    file_handler = open(path, 'w')
    json.dump(obj, file_handler)
    file_handler.close()

def mkdir(path):
    '''Creates folders if they dont exist'''
    dirname = ntpath.dirname(path)
    if not ntpath.exists(path):
        if dirname:
            os.makedirs(dirname)
            return True
    return False

def touch(path):
    '''Creates a file and associated folders if it doesnt exist'''
    if not ntpath.exists(path):
        mkdir(path)
        file_name = ntpath.basename(path)
        if file_name:
            open(path, 'w').close()
            return True
    return False

def change_ext(path, ext):
    '''Returns a string path with the extension swapped out'''
    return os.path.splitext(path)[0] + ext

