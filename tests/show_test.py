import os
import sys
import unittest
from unittest.mock import patch, PropertyMock
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

    def test_shows_with_no_new_episodes(self):
        '''Returns a dictionary of shows with new episodes'''
        print(self.shortDescription())

        # create shows that are identical in archive and online
        archived_episodes = {'prefix':'test_episode', 'count': 3}
        archived_shows = show_factory(archived_episodes, 'test_show', 2)

        available_episodes = {'prefix':'test_episode', 'count': 3}
        available_shows = show_factory(available_episodes, 'test_show', 2)


        show_with_new_episode = show.shows_with_new_episodes(available_shows, archived_shows)
        self.assertEqual(len(show_with_new_episode.keys()), 0, 'Dict should not have keys when archive matches available')
    
    def test_shows_with_new_episodes(self):
        '''Returns a dictionary of shows with new episodes'''
        print(self.shortDescription())

        # create shows that are identical in archive and online
        archived_episodes = {'prefix':'test_episode', 'count': 3}
        archived_shows = show_factory(archived_episodes, 'test_show', 2)

        available_episodes = {'prefix':'test_episode', 'count': 3}
        available_shows = show_factory(available_episodes, 'test_show', 2)

        
        # add a single show to have a new episode
        archived_show_with_old_episode = list(
            show_factory({'prefix':'test_episode', 'count': 3}, 'new_show', 1).values()
            )[0]

        show_with_new_episode = list(
            show_factory({'prefix':'test_episode', 'count': 4}, 'new_show', 1).values()
            )[0]

        archived_episodes[archived_show_with_old_episode.id] = archived_show_with_old_episode
        available_shows[show_with_new_episode.id] = show_with_new_episode
        show_with_new_episode = show.shows_with_new_episodes(available_shows, archived_shows)
        self.assertEqual(len(show_with_new_episode.keys()), 1, 'Should have one show with a new episode')

    def test_title_is_included(self):
        '''return a boolen if the title string is in the includes array'''
        print(self.shortDescription())
        title = 'foo'
        has_foo = ['bar', 'foo', 'baz']
        no_foo = ['bar', 'baz', 'boo']
        self.assertTrue(show.title_is_included(title, has_foo))
        self.assertFalse(show.title_is_included(title, no_foo))
    
    @patch('show.title_is_included')
    @patch('show.Episode.title', new_callable=PropertyMock)
    @patch('show.Episode')
    @patch('show.parse_entry')
    def test_get_episodes_from_entries(self, mock_parse_entry, mock_Episode, mock_title, mock_title_included):
        '''Returns a list of episodes form the supplied entries'''
        entries = {'foo': 1, 'bar': 2}
        episodes = {'foo_episode': 1, 'bar_episode': 2}
        mock_parse_entry.return_value = episodes
        mock_title.return_value = 'TITLE'

        output = show.get_episodes_from_entries(entries, [])
        self.assertEqual(
            len(output),
            len(entries.keys()), 
            'Count of Episodes returned should match entries sent when includes is empty'
        )

        mock_title_included.return_value = True
        output = show.get_episodes_from_entries(entries, ['foo'])
        self.assertEqual(
            len(output),
            2, 
            'Episodes should be returned when titles include check passes'
        )

        mock_title_included.return_value = False
        output = show.get_episodes_from_entries(entries, ['foo'])
        self.assertEqual(
            len(output),
            0, 
            'No episodes should be returned when titles include check fails'
        )
        # mock_parse_entry.assert_called()
        # self.assertTrue(mock_parse_entry.called)
        # self.assertEqual(mock_parse_entry.call_count, 2)
        
        # self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()