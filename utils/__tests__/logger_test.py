import os
import pytest
import logging
from utils.logger import logConfigFile
from unittest.mock import patch
from utils.logger import initLogging


def test_loglevel():
  """ Sets proper log level """
  initLogging()
  logger = logging.getLogger("tubular")
  assert logger.level == 10

def test_logConfigNotFound():
  patcher = patch('os.path.exists')
  mock_thing = patcher.start()
  mock_thing.side_effect = lambda path: False 
  initLogging()
  os.path.exists.assert_called_once_with(logConfigFile)
