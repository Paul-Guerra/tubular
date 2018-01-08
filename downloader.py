import os
import sys
import ntpath
import logging
import youtube_dl
from show import Show

logger = logging.getLogger('tubular')

AUDIO_QUALITY = '128'

class Downloader(object):

    def __init__(self):
        super().__init__()

        self.__temp_dir = 'tmp/'
        try:
            if not os.path.exists(self.__temp_dir):
                os.makedirs(self.__temp_dir)
        except (OSError, IOError) as err:
            logger.exception(str(err))
            sys.exit(1)

    def run(self, new_shows):
        downloaded_shows = []

        self.__empty_temp_dir()
        for _, show in new_shows.items():
            new_episodes = self.download_episodes(show.episodes)
            if new_episodes:
                downloaded_shows.append(
                    Show(show_id=show.id, title=show.title, episodes=new_episodes)
                )

        return downloaded_shows

    def youtube_dl_options(self, episode):
        # todo: see if option allows skipping the video download
        return {
            'ffmpeg_location': '/usr/local/bin/ffmpeg',
            'nocheckcertificate': True,
            'keepvideo': False,
            'outtmpl': '{dir}%(id)s'.format(dir=self.__temp_dir),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': AUDIO_QUALITY,
            }],
            'logger': logger,
            'progress_hooks': [lambda u: on_download_update(episode, u)]
        }

    def download_episodes(self, episodes):
        for e in episodes:
            options = self.youtube_dl_options(e)
            try:
                with youtube_dl.YoutubeDL(options) as ydl:
                    logger.info('Initiating download for episode %s (%s)', e.title, e.id)
                    ydl.download([e.web_page])
            except Exception as err:
                logger.exception(str(err))
        return list(filter(
            lambda e: e.download_finished is True,
            episodes)
        )
        
    def __empty_temp_dir(self):
        logger.info('Emptying {}'.format(self.__temp_dir))
        try:
            fileList = os.listdir(self.__temp_dir)
            for fileName in fileList:
                os.remove(self.__temp_dir + '/' + fileName)
        except OSError as e:
            logger.warn('Cannot empty {}. Error: {}'.format(self.__temp_dir, e))

def on_download_update(episode, u):
    if u['status'] is 'finished':
        logger.info('Download %s: Episode: "%s" (%s)', u['status'], episode.title, episode.id)
        logger.info(f'Download Data: {u}')
        episode.download_status = u
