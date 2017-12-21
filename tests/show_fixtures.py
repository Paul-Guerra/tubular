import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from episode import Episode
from show import Show

def episode_factory(prefix='', count=1, start=0):
    '''Returns a list of Episode object'''
    episodes = []
    for i in range(start, start + count):
        episodes.append(Episode({
            'id': f'{prefix}{i}',
            'title': f'{prefix}title_{i}',
            'web_page': f'{prefix}web_page_{i}',
            'description': f'{prefix}description_{i}',
            'video': f'{prefix}video_{i}',
            'thumbnail': f'{prefix}thumbnail_{i}',
        }))
    return episodes

def show_factory(episode_data, prefix='', count=1, start=0):
    '''Returns a dictionary of shows by id'''
    shows = {}
    for i in range(start, start + count):
        episodes = episode_factory(**episode_data)
        show = Show(show_id=f'{prefix}{i}', title=f'{prefix}title_{i}', episodes=episodes)
        shows[show.id] = show
    return shows
