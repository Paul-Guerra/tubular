'''
Functionality around publishing archived show data as a podcast
'''
import logging
from string import Template
from show import get_archived_shows

logger = logging.getLogger('tubular')

def show_as_podcast(show):
    print(channel_data(show))

def channel_data(show):
    try:
        with open('templates/channel_header.tpl', 'r') as ch:
            tpl = Template(ch.read())
            return tpl.substitute(
                title=show.title,
                link='http://placeholder',
                description='',
                thumbnail=show.episodes[0].thumbnail if show.episodes else ''
            )
    except (OSError, IOError) as err:
        logger.exception(str(err))


archived_shows = list(get_archived_shows().values())
# id, show = archived_shows
print(channel_data(archived_shows[0]))

