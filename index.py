import platform
import logging
from config import load as load_config
import youtube
from show import (
    feeds_to_shows,
    get_archived_shows,
    write_show_to_file,
    shows_with_new_episodes,
    archive_audio
)
from downloader import Downloader
from utils.logger import initLogging
import utils.files as uf

def main():
    data_dir = 'data/'
    initLogging()
    logger = logging.getLogger('tubular')

    uf.touch(data_dir)

    logger.info('Starting Tubular')
    logger.debug(f'Running on Python {platform.python_version()}')
    logger.debug(f'Log level set to {logger.level}')
    config = load_config()

    feeds = youtube.crawl(youtube.manifest(config))
    available_shows = feeds_to_shows(feeds)
    archived_shows = get_archived_shows()

    has_new_episodes = shows_with_new_episodes(available_shows, archived_shows)

    if len(has_new_episodes.keys()) is 0:
        logger.info('No New episodes found. Exiting')
        return

    dl_manager = Downloader()
    downloaded_shows = dl_manager.run(has_new_episodes)
    add_new_episodes(downloaded_shows, archived_shows)

    for show in archived_shows.values():
        write_show_to_file(show, f'{data_dir}/{show.id}.json')
        archive_audio(show, data_dir)

def add_new_episodes(downloaded_shows, archived_shows):
    for show in downloaded_shows:
        if show.id not in archived_shows:
            archived_shows[show.id] = show
        else:
            archive = archived_shows[show.id]
            archive.add_new_episodes(show.episodes)


main()