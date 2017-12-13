class Show(object):

  def __init__(self, title='Default Title', episodes=[]):
    self.title = title
    self.episodes = episodes

  def __str__(self):
    return 'Title: {}, Latest Episode: {},  Episodes[{}]'.format(self.title, self.episodes[0].title, len(self.episodes))

  def __repr__(self):
    return self.__str__()
