import os
import sys
import unittest
from show_fixtures import episode_factory, show_factory

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import show
from show import Show

class TestShow(unittest.TestCase):

    def test_new_episodes(self):
        '''Return unarchived episodes of a show'''
        print(self.shortDescription())

        archived_episodes = {'prefix':'test_episode', 'count': 3}
        archived_shows = show_factory(archived_episodes, 'test_show')

        available_episodes = {'prefix':'test_episode', 'count': 4}
        available_shows = show_factory(available_episodes, 'test_show')
        curr_show = list(available_shows.values())[0]

        new_episodes = show.new_episodes(curr_show, archived_shows)
        self.assertEqual(len(new_episodes), 1)
        self.assertEqual(next(iter(new_episodes)).id, 'test_episode3')

    def test_new_show(self):
        '''Return all episodes of a new (unarchived) show'''
        print(self.shortDescription())

        available_episodes = {'prefix':'test_episode', 'count': 4}        
        available_shows = show_factory(available_episodes, 'test_show')
        curr_show = list(available_shows.values())[0]

        new_episodes = show.new_episodes(curr_show, {})
        self.assertEqual(len(new_episodes), 4)

if __name__ == '__main__':
    unittest.main()