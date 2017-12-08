import os
import logging
import utils.logger
from unittest.mock import patch, mock_open

@patch('utils.logger.initBasicLogging')
@patch('utils.logger.initLoggingFromFile')
@patch('os.path.exists', return_value=False)
def test_logConfigNotFound(mock_exists, mock_file, mock_basic):
  utils.logger.initLogging()
  os.path.exists.assert_called_once_with(utils.logger.logConfigFile)
  utils.logger.initLoggingFromFile.assert_not_called()
  utils.logger.initBasicLogging.assert_called_once_with()

@patch('utils.logger.initBasicLogging')
@patch('utils.logger.initLoggingFromFile')
@patch('os.path.exists', return_value=True)
def test_logConfigFile(mock_exists, mock_file, mock_basic):
  utils.logger.initLogging()
  os.path.exists.assert_called_once_with(utils.logger.logConfigFile)
  utils.logger.initLoggingFromFile.assert_called_once_with(utils.logger.logConfigFile)
  utils.logger.initBasicLogging.assert_not_called()

@patch('logging.basicConfig')
@patch('os.path.exists', return_value=True)
def test_initBasicLogging(mock_exists, mock_basic_config):
  utils.logger.initBasicLogging()
  logging.basicConfig.assert_called_once_with()


# m = mock_open()
# @patch('__main__.open')
@patch('json.load')
@patch('logging.config.dictConfig')
def test_initLoggingFromFile(mock_json_load, mock_dictConfig):
  logConfig = { log: true }
  jsonLoadResult = { loaded: true }
  with patch('utils.logger.open', mock_open(read_data='bar'), create=True) as m:
    utils.logger.initLoggingFromFile('foo')
    m.assert_called_once_with('foo', 'r')

# def test_logConfigNotFound():
#   patcher = patch('os.path.exists')
#   patcher.start().side_effect = lambda path: False
#   utils.logger.initLogging()
#   os.path.exists.assert_called_once_with(utils.logger.logConfigFile)
#   patcher.stop()

# def test_loglevel():
#   ''' Sets proper log level '''
#   utils.logger.initLogging()
#   logger = logging.getLogger('tubular')
#   assert logger.level == 10