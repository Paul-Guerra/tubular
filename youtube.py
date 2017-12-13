import logging
import requests
from crawl_response import CrawlResponse
logger = logging.getLogger('tubular')

def crawl(manifest):
  return list(filter(lambda r: r is not None, map(fetch, manifest)))


def fetch(url):
  try:
    logger.info('Making request to {}'.format(url))
    response = requests.get(url, timeout=5)
    if response.status_code is not 200:
      logger.warn('Received non 200 response code for {}. Status Code:{}'.format(url, response.status_code))
      return None
    return CrawlResponse(response)
  except Exception:
    logger.exception('Error fetching response: {}'.format(url))

