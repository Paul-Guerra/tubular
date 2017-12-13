import xmltodict

class CrawlResponse(object):

  def __init__(self, response):
    if response is None:
      raise Exception('CrawlResponse requires a response object. "None" provided')
    self.response = response

  @property
  def response(self):
    return self.__response

  @response.setter
  def response(self, response):
    self.__xml = xmltodict.parse(response.text)

  @property
  def xml(self):
    return self.__xml

  @property
  def title(self):
    return self.__xml['feed']['title'] or 'Default title'

  @property
  def entries(self):
    return self.__xml['feed']['entry']

