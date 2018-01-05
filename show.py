'''
Show class an related utility functions
'''

import os
import json
import logging
import utils.files as uf
from episode import Episode, parse_entry

logger = logging.getLogger('tubular')

class Show(object):
    '''
    Class for a show object as populated from crawl responses
    '''

    def __init__(self, show_id, title, episodes):
        super().__init__()

        self.__id = show_id
        self.__title = title
        self.__episodes = episodes or []

    @property
    def id(self):
        '''Read-only id of the show'''
        return self.__id

    @property
    def title(self):
        '''Read-only title of the show'''
        return self.__title

    @property
    def episodes(self):
        ''' Read-only access to episodes property'''
        return list(self.__episodes)
    
    def add_episodes(self, new_episodes):
        '''Appends new episodes to the existing episodes'''
        self.__episodes += new_episodes

    def to_dict(self):
        '''Returns the show as a dictionary'''
        return {
            'id': self.id,
            'title': self.title,
            'episodes': list(map(lambda e: e.to_dict(), self.episodes))
        }

    @staticmethod
    def hydrate(show_dict):
        '''Creates a new Shor object from a compaitible dictionary'''
        episodes = [Episode(e) for e in show_dict['episodes']]
        return Show(show_id=show_dict['id'], title=show_dict['title'], episodes=episodes)

def write_show_to_file(show, path):
    '''Writes a show to a file at the given path in JSON'''
    if not show:
        return None

    try:
        uf.write_dict_as_json(show.to_dict(), path)
    except Exception as e:
        logger.warn('Error writing {}. Error: {}'.format(path, str(e)))
        return None

def open_show_from_file(path):
    '''Return a show object using data stored in the file found at path'''
    if not path:
        return None

    try:
        data = uf.open_json_as_dict(path)
        return Show.hydrate(data)
    except Exception as e:
        logger.warn('Error opening {}. Error: {}'.format(path, str(e)))
        return None


def get_archived_shows(path='data/'):
    '''Returns dictionary of shows previously downloaded'''

    shows = {}
    file_list = list(filter(lambda f: os.path.isfile(f'{path}{f}'), os.listdir(path)))
    for f in file_list:
        show = open_show_from_file('{}{}'.format(path, f))
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
            get_episodes_from_entries(f.entries, f.manifest_item.include)
        )

    return shows

def get_episodes_from_entries(entries, includes):
    '''
    Return a list of episodes from the provided entries 
    that include one the specified "include" strings
    '''

    entries_dict = list(map(parse_entry, entries))
    episodes = list(map(Episode, entries_dict))
    if not includes:
        return episodes

    includes = list(map(lambda i: i.lower(), includes))
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
    for show in list(available_shows.values()):
        episodes = new_episodes(show, archived_shows)
        if episodes:
            shows[show.id] = Show(show.id, show.title, episodes)

    return shows

def new_episodes(available_show, archived_shows):
    '''
    For the given available show find the matching archived_show (if available)
    and return a list of new episodes (not in the archived show)
    '''
    if available_show.id not in archived_shows:
        return available_show.episodes
    
    archived_show = archived_shows[available_show.id]
    return list(set(available_show.episodes) - set(archived_show.episodes))

def archive_audio(show, data_dir) :
    '''Moves audio files from given temp directory to archive directory'''
    try:
        dir_path = f'{data_dir}{show.id}/'
        uf.mkdir(dir_path)
        for e in show.episodes:
            e.archive_audio(f'{dir_path}{e.id}.mp3') 
    except (OSError, IOError) as err:
        logger.exception(str(err))
