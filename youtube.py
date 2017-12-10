def get_user_urls(config):
  if config is None or config['youtube']['user_url'] is None:
    return false
  
  urls = []
  for chan in config['channels']:
    urls.append('{}{}'.format(config['youtube']['user_url'], chan['user']))
  
  return urls

def fetch_urls():
  return False

def fetch():
  return False