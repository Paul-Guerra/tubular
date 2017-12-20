import unittest
import os
import logging
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.logger

jsonLoadResult = { 'loaded': True }

def oserr(e): 
  raise OSError

def ioerr(e): 
  raise IOError

class TestLogger(unittest.TestCase):
  @patch('utils.logger.initBasicLogging')
  @patch('utils.logger.initLoggingFromFile')
  @patch('os.path.exists', return_value=False)
  def test_logConfigNotFound(self, mock_exists, mock_file, mock_basic):
    '''Call basic config when file is not found'''
    print(self.shortDescription())
    utils.logger.initLogging()
    os.path.exists.assert_called_once_with(utils.logger.logConfigFile)
    utils.logger.initLoggingFromFile.assert_not_called()
    utils.logger.initBasicLogging.assert_called_once_with()

  @patch('utils.logger.initBasicLogging')
  @patch('utils.logger.initLoggingFromFile')
  @patch('os.path.exists', return_value=True)
  def test_logConfigFile(self, mock_exists, mock_file, mock_basic):
    '''Calls initLoggingFromFile by when file exists'''
    print(self.shortDescription())
    utils.logger.initLogging()
    os.path.exists.assert_called_once_with(utils.logger.logConfigFile)
    utils.logger.initLoggingFromFile.assert_called_once_with(utils.logger.logConfigFile)
    utils.logger.initBasicLogging.assert_not_called()

  @patch('logging.basicConfig')
  @patch('os.path.exists', return_value=True)
  def test_initBasicLogging(self, mock_exists, mock_basic_config):
    '''Calls logging.basicConfig'''
    print(self.shortDescription())
    utils.logger.initBasicLogging()
    logging.basicConfig.assert_called_once_with()


  @patch('logging.config.dictConfig')
  @patch('json.load', return_value=jsonLoadResult)
  def test_initLoggingFromFile(self, mock_json_load, mock_dictConfig):
    '''Creates logger from config file'''
    print(self.shortDescription())
    with patch('utils.logger.open', mock_open(read_data='bar'), create=True) as m:
      utils.logger.initLoggingFromFile('path/to/file')
      m.assert_called_once_with('path/to/file', 'r')
      mock_dictConfig.assert_called_once_with(jsonLoadResult)

  @patch('utils.logger.initBasicLogging')
  @patch('logging.config.dictConfig', side_effect=ioerr)
  @patch('json.load', return_value=jsonLoadResult)
  def test_catchIOError(self, mock_json_load, mock_dictConfig, mock_basicLogging):
    '''Calls basic logger if there is an IO exception'''
    print(self.shortDescription())
    with patch('utils.logger.open', mock_open(read_data='bar'), create=True) as m:
      utils.logger.initLoggingFromFile('path/to/file')
      mock_basicLogging.assert_called_once_with()

  @patch('utils.logger.initBasicLogging')
  @patch('logging.config.dictConfig', side_effect=oserr)
  @patch('json.load', return_value=jsonLoadResult)
  def test_catchOSError(self, mock_json_load, mock_dictConfig, mock_basicLogging):
    '''Calls basic logger if there is an OS exception'''
    print(self.shortDescription())
    with patch('utils.logger.open', mock_open(read_data='bar'), create=True) as m:
      utils.logger.initLoggingFromFile('path/to/file')
      mock_basicLogging.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()