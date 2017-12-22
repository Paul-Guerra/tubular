import platform
import logging
from config import load as load_config
import youtube
from show import (
    feeds_to_shows,
    get_archived_shows,
    shows_with_new_episodes
)
from downloader import Downloader
from utils.logger import initLogging
import utils.files as uf

def main():
    initLogging()
    logger = logging.getLogger('tubular')

    uf.touch('data/')

    logger.info('Starting Tubular')
    logger.debug('Running on Python {}'.format(platform.python_version()))
    logger.debug('Log level set to {}'.format(logger.level))
    config = load_config()

    feeds = youtube.crawl(youtube.manifest(config))
    available_shows = feeds_to_shows(feeds)
    archived_shows = get_archived_shows()

    has_new_episodes = shows_with_new_episodes(available_shows, archived_shows)

    dl_manager = Downloader()
    downloaded_shows = dl_manager.run(has_new_episodes)
    add_new_episodes(downloaded_shows, archived_shows)

    print('archived_shows', archived_shows)

    print(downloaded_shows[0].to_json())

def add_new_episodes(downloaded_shows, archived_shows):
    for show in downloaded_shows:
        if show.id not in archived_shows:
            archived_shows[show.id] = show
        else:
            archive = archived_shows[show.id]
            archive.add_new_episodes(show.episodes)


main()