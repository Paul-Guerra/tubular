class Episode(object):

  def __init__(self, data):
    self.__data = dict(data)

  def __hash__ (self):
    return hash(self.id)

  def __eq__ (self, other):
    return hash(self.id) == hash(other.id)
    
  def __ne__ (self, other):
    return not self.__eq__(other)

  @property
  def id(self):
    return self.__data['id']

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
