'''
Episode class and related helper function, parse_entry, used for coverting data from the XML feed
'''

class Episode(object):
    '''
    An entry on a channel. All properties are immutable and based on a dict sent to the constructor
    '''
    def __init__(self, data):
        self.__data = dict(data)
        super().__init__()


    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(other) is type(self) and hash(self.id) == hash(other.id)

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def id(self):
        '''Id of episode. should match the video id from the feed'''
        return self.__data['id']

    @property
    def title(self):
        '''Title of episode. Should match the Title from the feed'''
        return self.__data['title']

    @property
    def web_page(self):
        '''The URL the episode video can be viewed'''
        return self.__data['web_page']

    @property
    def description(self):
        '''The episode description'''
        return self.__data['description']

    @property
    def video(self):
        '''URL to the video file'''
        return self.__data['video']

    @property
    def thumbnail(self):
        '''URL to the episode thumbnail'''
        return self.__data['thumbnail']


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
