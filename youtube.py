import requests
import logging

logger = logging.getLogger('tubular')

def get_user_urls(config):
  if config is None:
    return False

  if 'user_url' not in config['youtube']:
    return False

  urls = []
  for chan in config['channels']:
    urls.append('{}{}'.format(config['youtube']['user_url'], chan['user']))
  
  return urls

def fetch_urls(urls):
  return map(fetch, urls)

def fetch(url):
  logger.info('Making request to {}'.format(url))
  return requests.get(url, timeout=5)