'''
Functionality around writing archived show data as a podcast
'''
import logging
from string import Template
from os.path import getsize
from xml.sax.saxutils import escape
from utils.files import mkdir
from show import get_archived_shows
from downloader import AUDIO_QUALITY as kbps
from config import load as load_config
from episode import audio_path_to_url

logger = logging.getLogger('tubular')

def write(show, podcast_dir):
    try:
        mkdir(podcast_dir)
        content = show_as_podcast(show)
        with open(f'{podcast_dir}{show.id}.xml', 'w') as f:
            f.write(content)
    except (OSError, IOError) as err:
        logger.exception(str(err))
    finally:
        f.close()

def show_as_podcast(show):
    base_audio_url = load_config()['base_audio_url']
    channel = channel_view(show)
    items = items_view(show, base_audio_url)
    return rss_view(channel, items)

def rss_view(channel_data, items):
    rss = ''
    try:
        with open('templates/rss.tpl', 'r') as f:
            tpl = Template(f.read())
            rss =  tpl.substitute(
                channel_data=channel_data,
                items=items
            )
    except (OSError, IOError, TypeError, ValueError) as err:
        logger.exception(str(err))
    finally:
        f.close()
    
    return rss

def channel_view(show):
    channel = ''
    try:
        with open('templates/channel_header.tpl', 'r') as f:
            tpl = Template(f.read())
            channel =  tpl.substitute(
                title=escape(show.title),
                link='http://placeholder',
                description='',
                thumbnail=show.episodes[0].thumbnail if show.episodes else ''
            )
    except (OSError, IOError, TypeError, ValueError) as err:
        logger.exception(str(err))
    finally:
        f.close()

    return channel

def items_view(show, base_audio_url):
    items = []
    try:
        episodes_by_date = sorted(show.episodes, key=lambda e: e.date, reverse=True)
        with open('templates/channel_item.tpl', 'r') as f:
            tpl = Template(f.read())
            for episode in episodes_by_date:
                length_bytes = getsize(episode.audio_path)
                length_seconds = int(length_bytes * .008 / int(kbps))
                items.append(tpl.substitute(
                    id=escape(episode.id),
                    title=escape(episode.title),
                    pubdate=episode.date,
                    audio_url=audio_path_to_url(episode.audio_path, base_audio_url),
                    description=escape(episode.description),
                    thumbnail=episode.thumbnail if show.episodes else '',
                    length_bytes=length_bytes,
                    length_seconds=length_seconds
                ))
    except (OSError, IOError, TypeError, ValueError) as err:
        logger.exception(str(err))
    finally:
        f.close()

    return str().join(items)


if __name__ == '__main__':
    archived_shows = list(get_archived_shows().values())
    for show in archived_shows:
      write(show, load_config()['podcast_dir'])
