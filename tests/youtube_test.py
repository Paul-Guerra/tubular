import os
import sys
import unittest
from unittest.mock import patch, Mock
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import youtube


class TestYouTube(unittest.TestCase):
    def test_noneAsConfig(self):
        '''youtube::manifest returns False if config is None'''
        print(self.shortDescription())
        output = youtube.manifest(None)    
        self.assertFalse(output, 'Returns False if config is not provided')

    def test_urlIsNone(self):
        '''youtube::manifest returns False if youtube.user_url is None'''
        print(self.shortDescription())
        badConfig = {'youtube': {'foo': True}}
        output = youtube.manifest(badConfig)    
        self.assertFalse(output, 'Youtube user_url section in config is required')

    def test_youtubeConfigIsBad(self):
        '''youtube::manifest returns False if youtube is None'''
        print(self.shortDescription())
        badConfig = {'channels': {'foo': True}}
        output = youtube.manifest(badConfig)    
        self.assertFalse(output, 'Youtube section in config is required')

    @patch('youtube.ManifestItem', return_value='ManifestItem')
    def test_urlsList(self, manifest_item):
        '''youtube::get_user_urls returns a list of urls'''
        print(self.shortDescription())
        config = {
            'youtube': {'user_url': 'foo'},
            'channels': [{'user': 'bar'}]
            }

        output = youtube.manifest(config)    
        self.assertEqual(type(output), list)
        self.assertEqual(manifest_item.call_count, len(config['channels']), 'Creates a ManifestItem for each channel in config')

    @patch('youtube.logger')
    @patch('requests.get')
    def test_fetchURL(self, mock_get, logger):
        '''youtube::fetch makes request to URL'''
        print(self.shortDescription())


        item = Mock(url='foo')
        data = youtube.fetch(item)
        mock_get.assert_called_with('foo', timeout=5)
        logger.warning.assert_called()

    @patch('youtube.CrawlResponse', return_value='CrawlResponse')
    @patch('requests.get')
    def test_fetchReturnsResponse(self, mock_get, crawl_response):
        '''youtube::fetch returns response from request'''
        print(self.shortDescription())

        item = Mock()
        item.url.return_value = 'foo'
        response = Mock()
        response.status_code = 200
        mock_get.return_value = response
        data = youtube.fetch(item)
        # self.assertEqual(data, response)
        crawl_response.assert_called()


    @patch('youtube.logger')
    @patch('requests.get', side_effect=Exception('oops'))
    def test_fetch_error(self, mock_get, logger):
        '''youtube::Logs Request Exceptions'''
        print(self.shortDescription())

        item = Mock(url='foo')
        data = youtube.fetch(item)
        logger.exception.assert_called()
        self.assertIsNone(data, 'Returns None on error')

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