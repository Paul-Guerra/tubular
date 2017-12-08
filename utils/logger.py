import os
import json
import logging
import logging.config

logConfigFile = 'utils/logger.json'

def initLogging(path=logConfigFile):
  if os.path.exists(path):
    initLoggingFromFile(path)
  else:
    initBasicLogging()

def initLoggingFromFile(path=logConfigFile):
  with open(path, 'r') as f:
    config = json.load(f)
  logging.config.dictConfig(config)

def initBasicLogging():
  logging.basicConfig()
