class Episode(object):

  def __init__(self, data):
    self.__data = data
    self.downloaded = False
    self.uploaded = False
    self.tmp_path = None

  @property
  def title(self):
    return self.__data['title']

  @property
  def web_page(self):
    return self.__data['web_page']

  @property
  def description(self):
    return self.__data['description']

  @property
  def video(self):
    return self.__data['video']

  @property
  def thumbnail(self):
    return self.__data['thumbnail']

  @property
  def id(self):
    return self.__data['id']

def parse_entry(xmldict):
  '''
  Takes an XML dictioanry object of an atom feed entry and returns an episode data dict
  '''
  return {
    'id': xmldict['yt:videoId'],
    'title': xmldict['media:group']['media:title'],
    'web_page': xmldict['link']['@href'],
    'description': xmldict['media:group']['media:description'],
    'thumbnail': xmldict['media:group']['media:thumbnail']['@url'],
    'video': xmldict['media:group']['media:content']['@url'],
  }
