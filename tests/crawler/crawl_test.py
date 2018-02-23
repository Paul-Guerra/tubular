import os
import sys
import unittest
from unittest.mock import patch, Mock, MagicMock
import asyncio

import crawler.crawl as crawl

def async_mock(*args, **kwargs):
    m = MagicMock(*args, **kwargs)
    async def coro(*args, **kwargs):
        return m(*args, **kwargs)

    coro.mock = m
    return coro


class CrawlTest(unittest.TestCase):

    @patch('crawler.crawl.fetch_urls')
    @patch('asyncio.get_event_loop')
    def test_get(self, get_event_loop, m_fetch_urls):
        m_loop = Mock()
        get_event_loop.return_value = m_loop
        manifest = ['url1', 'url2']

        crawl.get(manifest)

        self.assertTrue(get_event_loop.called, 'Starts an asyncio event loop')
        m_fetch_urls.assert_called_with(m_loop, manifest)
        self.assertTrue(m_loop.close.called, 'Waits for loop to end')

    @patch('crawler.crawl.fetch', new_callable=async_mock)
    def test_fetch_urls(self, m_fetch):
        manifest = ['url1', 'url2']    
        loop = asyncio.new_event_loop()
        results = loop.run_until_complete(crawl.fetch_urls(loop, manifest))
        loop.close()

        self.assertEqual(m_fetch.mock.call_count, 2, 'Called fetch twice')
        self.assertEqual(len(results), 2, 'Returned 2 results')

    @patch('requests.get')
    def test_fetch(self, requests_get):
        url = 'url'
        m_response = Mock()
        requests_get.return_value = m_response
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(crawl.fetch(url))
        loop.close()

        requests_get.assert_called_with(url, timeout=5)
        self.assertIs(result['url'], url, 'Returns formated result with url')
        self.assertIs(result['response'], m_response, 'Returns formated result with response')


    @patch('requests.get', side_effect=Exception('oops'))
    def test_fetch_fail(self, m_get):
        url = 'url'
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(crawl.fetch(url))
        loop.close()

        self.assertEqual(result, None, 'Returns None if error')

if __name__ == '__main__':
    unittest.main()