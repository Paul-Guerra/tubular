'''
Episode class and related helper function, parse_entry, used for coverting data from the XML feed
'''

import json

class Episode(object):
    '''
    An entry on a channel. All properties are immutable and based on a dict sent to the constructor
    '''
    def __init__(self, data):
        super().__init__()

        self.__id = data['id']
        self.__title = data['title']
        self.__web_page = data['web_page']
        self.__description = data['description']
        self.__video = data['video']
        self.__thumbnail = data['thumbnail']
        self.download_status = {}

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(other) is type(self) and hash(self.id) == hash(other.id)

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def id(self):
        '''Id of episode.'''
        return self.__id

    @property
    def title(self):
        '''Title of episode.'''
        return self.__title

    @property
    def web_page(self):
        '''The URL the episode video can be viewed'''
        return self.__web_page

    @property
    def description(self):
        '''The episode description'''
        return self.__description

    @property
    def video(self):
        '''URL to the video file'''
        return self.__video

    @property
    def thumbnail(self):
        '''URL to the episode thumbnail'''
        return self.__thumbnail


def parse_entry(xmldict):
    '''
    Takes an XML dictionary object of an atom feed entry and returns an episode data dict
    '''
    return {
        'id': xmldict['yt:videoId'],
        'title': xmldict['media:group']['media:title'],
        'web_page': xmldict['link']['@href'],
        'description': xmldict['media:group']['media:description'],
        'thumbnail': xmldict['media:group']['media:thumbnail']['@url'],
        'video': xmldict['media:group']['media:content']['@url'],
    }
