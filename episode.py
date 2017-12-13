class Episode(object):

  def __init__(self, entry):
    self.__entry = entry

  @property
  def entry(self):
    return self.__entry

  @property
  def title(self):
    return self.__entry['media:group']['media:title']

  @property
  def web_page(self):
    return self.__entry['link']['@href']

  @property
  def description(self):
    return self.__entry['media:group']['media:description']

  @property
  def video(self):
    return self.__entry['media:group']['media:content']['@url']

  @property
  def thumbnail(self):
    return self.__entry['media:group']['media:thumbnail']['@url']

  @property
  def id(self):
    return self.__entry['yt:videoId']
