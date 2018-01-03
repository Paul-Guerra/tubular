import os
import sys
import unittest
from unittest.mock import patch, Mock
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import youtube


class TestYouTube(unittest.TestCase):
  def test_noneAsConfig(self):
    '''youtube::get_user_urls returns False if config is None'''
    print(self.shortDescription())
    output = youtube.crawl(None)    
    self.assertEqual(output, False)

  def test_urlIsNone(self):
    '''youtube::get_user_urls returns False if youtube.user_url is None'''
    print(self.shortDescription())
    badConfig = {'youtube': {'foo': True}}
    output = youtube.crawl(badConfig)    
    self.assertEqual(output, False)
  
  def test_urlsList(self):
    '''youtube::get_user_urls returns a list of urls'''
    print(self.shortDescription())
    config = {
      'youtube': {'user_url': 'foo'},
      'channels': [{'user': 'bar'}]
      }

    output = youtube.crawl(config)    
    self.assertEqual(type(output), list)
    self.assertEqual(output[0], 'foobar')
  
  @patch('requests.get')
  def test_fetchURL(self, mock_get):
    '''youtube::fetch makes request to URL'''
    print(self.shortDescription())

    data = youtube.fetch('foo')
    mock_get.assert_called_with('foo', timeout=5)


  @patch('requests.get')
  def test_fetchReturnsResponse(self, mock_get):
    '''youtube::fetch returns response from request'''
    print(self.shortDescription())

    response = Mock()
    mock_get.return_value = response
    data = youtube.fetch('foo')
    self.assertEqual(data, response)
  
  @patch('youtube.map')
  @patch('youtube.fetch')
  def test_fetch_urls_maps(self, mock_fetch, mock_map):
    '''youtube::fetch_url maps over the URLs'''
    print(self.shortDescription())

    urls = ['foo']
    youtube.crawl(urls)
    mock_map.assert_called_with(mock_fetch, urls)

if __name__ == '__main__':
  unittest.main()