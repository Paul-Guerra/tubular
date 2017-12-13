from show import Show
from episode import Episode

class Subscriptions(object):

  def __init__(self, feeds):
    self.__shows = feeds_to_shows(feeds)

  def __str__(self):
    output = ''
    for show in self.shows:
        output += str(show)

    return output

  @property
  def shows(self):
    return self.__shows

def feeds_to_shows(feeds):
  return list(map(lambda f: Show(f.title, get_episodes(f)), feeds))

def get_episodes(response):
  return list(map(Episode, response.entries))

