'''
Show class an related utility functions
'''

import os
import logging
import utils.files as uf
from episode import Episode, parse_entry

logger = logging.getLogger('tubular')

class Show(object):
    '''
    Class for a show object as populated from crawl responses
    '''

    def __init__(self, id, title, episodes):
        self.title = title
        self.__id = id
        self.__episodes = episodes or []
        self.__episodes_by_id = {}
        self.__index_episodes(episodes)

    def __index_episodes(self, episodes):
        for e in episodes:
            self.__episodes_by_id[e.id] = e
    
    @property
    def id(self):
        '''Read-only id of the show'''
        return self.__id

    @property
    def episodes(self):
        ''' Read-only access to episodes property'''
        return self.__episodes

    @property
    def downloaded_episodes(self):
        '''Returns a list of episodes marked as downloaded'''
        return list(filter(
            lambda e: e.downloaded is True,
            self.__episodes
        ))

    @property
    def episodes_by_id(self):
        '''Returns a dictionary of episodes using their id as the key'''
        return self.__episodes_by_id

    @property
    def episode_ids(self):
        '''Returns all episode ids'''
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


def open_show_from_file(path):
    '''Return a show object using data stored in the file found at path'''
    try:
        data = uf.open_json_as_dict(path)
    except Exception as e:
        logger.warn('Error opening {}. Returning "None"'.format(path))
        return None

    return Show(id=data["id"], title=data['title'], episodes=data['episodes'])

def get_archived_shows(dir='data/'):
    '''Shows previously downloaded and published'''

    shows = {}
    fileList = os.listdir(dir)
    for f in fileList:
        show = open_show_from_file('{}/{}'.format(dir, f))
        if show is not None:
            shows[show.id] = show
    return shows


def feeds_to_shows(feeds):
    '''Converts feeds data into a dictionary or show objects'''
  
    shows = {}
    for f in feeds:
         shows[f.manifest_item.id] = Show(
             f.manifest_item.id,
             f.manifest_item.title,
             get_episodes_from_entries(f)
            )

    return shows

def get_episodes_from_entries(feed_response):
    '''
    Return a list of episodes from the provided entries 
    that include one the specified "include" strings
    '''

    entries_dict = list(map(parse_entry, feed_response.entries))
    episodes = list(map(Episode, entries_dict))
    includes = list(map(
        lambda i: i.lower(),
        feed_response.manifest_item.include
        ))
    return list(filter(
        lambda e: title_is_included(e.title.lower(), includes),
        episodes
    ))

def title_is_included(title, includes):
    '''Returns True if one of the include list strings is in the title'''
    for i in includes:
        if i in title:
            return True 
    return False

def shows_with_new_episodes(available_shows, archived_shows):
    '''Returns a dictionary of show ids that map to show object containing new episodes'''
    shows = {}
    for show in available_shows:
        episodes = new_episodes(show, archived_shows[show.id])
        if count(episodes) > 0:
            shows[show.id] = Show(show.id, show.title, episodes)

    return shows

def new_episodes(available_show, archived_shows):
    '''
    For the given available show find the matching archived_show (if available)
    and return a list of new episodes (not in the archived show)
    '''
    if available_show.id not in archived_shows:
        return available_show
    
    archived_show = archived_shows[available_show.id]