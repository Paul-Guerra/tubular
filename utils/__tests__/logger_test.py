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

jsonLoadResult = { 'loaded': True }

@patch('logging.config.dictConfig')
@patch('json.load', return_value=jsonLoadResult)
def test_initLoggingFromFile(mock_json_load, mock_dictConfig):
  with patch('utils.logger.open', mock_open(read_data='bar'), create=True) as m:
    utils.logger.initLoggingFromFile('path/to/file')
    m.assert_called_once_with('path/to/file', 'r')
    mock_dictConfig.assert_called_once_with(jsonLoadResult)

def oserr(e): 
  raise OSError

def ioerr(e): 
  raise IOError

@patch('utils.logger.initBasicLogging')
@patch('logging.config.dictConfig', side_effect=ioerr)
@patch('json.load', return_value=jsonLoadResult)
def test_catchIOError(mock_json_load, mock_dictConfig, mock_basicLogging):
  with patch('utils.logger.open', mock_open(read_data='bar'), create=True) as m:
    utils.logger.initLoggingFromFile('path/to/file')
    mock_basicLogging.assert_called_once_with()

@patch('utils.logger.initBasicLogging')
@patch('logging.config.dictConfig', side_effect=ioerr)
@patch('json.load', return_value=jsonLoadResult)
def test_catchOSError(mock_json_load, mock_dictConfig, mock_basicLogging):
  with patch('utils.logger.open', mock_open(read_data='bar'), create=True) as m:
    utils.logger.initLoggingFromFile('path/to/file')
    mock_basicLogging.assert_called_once_with()
