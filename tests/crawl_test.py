import os
import sys
import unittest
from unittest.mock import patch, Mock, MagicMock
import asyncio

# sys.path.insert(0, f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/tubular')
import crawl

def async_mock(*args, **kwargs):
    m = MagicMock(*args, **kwargs)
    async def coro(*args, **kwargs):
        return m(*args, **kwargs)

    coro.mock = m
    return coro


class CrawlTest(unittest.TestCase):

    @patch('crawl.crawl')
    @patch('asyncio.get_event_loop')
    def test_main(self, get_event_loop, m_crawl):
        m_loop = Mock()
        get_event_loop.return_value = m_loop
        manifest = ['url1', 'url2']

        crawl.main(manifest)

        self.assertTrue(get_event_loop.called, 'Starts an asyncio event loop')
        m_crawl.assert_called_with(m_loop, manifest)
        self.assertTrue(m_loop.close.called, 'Waits for loop to end')

    @patch('crawl.fetch', new_callable=async_mock)
    def test_crawl(self, m_fetch):
        manifest = ['url1', 'url2']    
        loop = asyncio.new_event_loop()
        results = loop.run_until_complete(crawl.crawl(loop, manifest))
        # loop.close()

        self.assertEqual(m_fetch.mock.call_count, 2, 'Called fetch twice')
        self.assertEqual(len(results), 2, 'Returned 2 results')

    @patch('requests.get')
    def test_fetch(self, m_get):
        url = 'url'
        m_response = Mock()
        m_get.return_value = m_response
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(crawl.fetch(url))
        loop.close()

        m_get.assert_called_with(url, timeout=5)
        self.assertIs(result, m_response, 'Returns response from get()')


    @patch('requests.get', side_effect=Exception('oops'))
    def test_fetch_fail(self, m_get):
        url = 'url'
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(crawl.fetch(url))
        loop.close()

        self.assertEqual(result, None, 'Returns None if error')

if __name__ == '__main__':
  unittest.main()