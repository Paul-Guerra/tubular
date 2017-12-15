class ManifestItem(object):
  
  def __init__(self, channel, url_base):
    self.__channel = channel
    self.__url_base = url_base
  
  @property
  def url(self):
    return '{}{}'.format(self.__url_base, self.__channel['user'])
    
  @property
  def include(self):
    return self.__channel['include']

  @property
  def title(self):
    return self.__channel['title']
    
