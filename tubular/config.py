import os
import sys
import json
import logging
from utils.files import open_json_as_dict
logger = logging.getLogger('tubular')

def load():
    '''Loads a JSON config file as a dictionary'''
    try:
        return open_json_as_dict('./tubular/config.json')
    except (OSError, IOError) as err:
        logger.critical('Error loading app config: {}'.format(str(err)))
        sys.exit(1)
