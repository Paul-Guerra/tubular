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
import podcast

def main():
    initLogging()
    logger = logging.getLogger('tubular')
    try:
        logger.info('Starting Tubular')
        logger.debug(f'Running on Python {platform.python_version()}')
        logger.debug(f'Log level set to {logger.level}')
        app_config = load_config()

        uf.touch(app_config['data_dir'])
        uf.touch(app_config['audio_dir'])

        feeds = youtube.crawl(youtube.manifest(app_config))
        available_shows = feeds_to_shows(feeds)
        archived_shows = get_archived_shows(app_config['data_dir'])

        has_new_episodes = shows_with_new_episodes(available_shows, archived_shows)

        if len(has_new_episodes.keys()) is 0:
            logger.info('No New episodes found. Exiting')
            return

        dl_manager = Downloader()
        downloaded_shows = dl_manager.run(has_new_episodes)
        add_new_episodes(downloaded_shows, archived_shows)
        write_archive(archived_shows, app_config)
    except Exception as err:
        logger.exception(str(err))

def write_archive(archived_shows, config):
    logger = logging.getLogger('tubular')    
    for show in archived_shows.values():
        logger.info(f'Archiving audio files for {show.id}')
        archive_audio(show, config['audio_dir'])
        logger.info(f'Archiving metadata for {show.id}')
        write_show_to_file(show, f'{config["data_dir"]}{show.id}.json')
        logger.info(f'writing podcast data for {show.id}')
        podcast.write(show, config['podcast_dir'])

def add_new_episodes(downloaded_shows, archived_shows):
    logger = logging.getLogger('tubular')    
    for show in downloaded_shows:
        if show.id not in archived_shows:
            logger.info('Adding new show to archive')
            archived_shows[show.id] = show
        else:
            logger.info(f'Adding {len(show.episodes)} new episodes to {show.id}')
            archive = archived_shows[show.id]
            archive.add_episodes(show.episodes)

main()

# initLogging()
# config = load_config()
# archived_shows = get_archived_shows(config['data_dir'])
# write_archive(archived_shows, config)
