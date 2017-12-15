class Show(object):

  def __init__(self, id, title='Default Title', episodes=[]):
    self.title = title
    self.__id = id
    self.__episodes = episodes
    self.__episodes_by_id = {}
    self.__index_episodes(episodes)
  
  def __str__(self):
    return 'Title: {}, Latest Episode: {},  Episodes[{}]'.format(self.title, self.__episodes[0].title, len(self.__episodes))

  def __repr__(self):
    return self.__str__()

  def __index_episodes(self, episodes):
    for e in episodes:
      self.__episodes_by_id[e.id] = e
  
  @property
  def episodes(self):
    return self.__episodes

  @property
  def downloaded_episodes(self):
    return filter(
      lambda e: e.downloaded is True
      self.__episodes
    )

  @property
  def episodes_by_id(self):
    return self.__episodes_by_id

  @property
  def episode_ids(self):
    return dict.keys(self.episodes_by_id)

  def get_episodes_by_id(self, ids):
    return list(map(
      lambda i: self.episodes_by_id[i],
      ids
    ))

  def get_new_episodes(self, previous_episode_ids):
    previous_ids = set(previous_episode_ids)
    episode_ids = set(self.episode_ids)
    new_episodes = episode_ids - previous_ids
    return self.get_episodes_by_id(list(new_episodes))