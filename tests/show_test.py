import os
import sys
import unittest
from unittest.mock import patch, Mock, PropertyMock

from show_fixtures import (episode_factory, show_factory, init_half_false, inc_ids)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import show
from show import Show

class TestShowFunctions(unittest.TestCase):

    def test_new_episodes(self):
        '''Returns unarchived episodes of a show'''
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
        '''Returns all episodes of a new (unarchived) show'''
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
        '''Returns a boolen if the title string is in the includes array'''
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
        print(self.shortDescription())
        
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

        # Only report that one episode passes the include filter
        mock_title_included.side_effect = [True, False] 
        output = show.get_episodes_from_entries(entries, ['foo'])
        self.assertEqual(
            len(output),
            1, 
            'Episodes should only be returned when titles include check passes'
        )

    @patch('show.get_episodes_from_entries', side_effect=lambda e, i: [])
    @patch('show.Show', side_effect=lambda id, title, episodes: True)
    @patch('crawl_response.CrawlResponse', autospec=True)
    def test_feeds_to_shows(self, mock_CrawlResponse, mock_Show, *args):
        '''Converts feeds to shows dictionary'''
        print(self.shortDescription())
        
        m1 = mock_CrawlResponse(response=Mock(), manifest_item=Mock())
        m2 = mock_CrawlResponse(response=Mock(), manifest_item=Mock())
        feeds = {
            'foo': m1,
            'bar': m2
        }
        output = show.feeds_to_shows(feeds)
        self.assertEqual(type(output), dict, 'Returns a dictionary')
        self.assertEqual(mock_Show.call_count, 2, 'Show is created for each feed')
        # self.assertEqual(len(output.values()), 2, 'Returns a show for every feed')

    @patch('os.listdir', return_value=[])
    def test_empty_archive_directory(self, listdir):
        '''Handles an empty directory'''
        print(self.shortDescription())
        
        shows = show.get_archived_shows()
        self.assertEqual(len(shows.keys()), 0, 'No shows returns if no files are in directory')

    @patch('os.listdir', return_value=['a', 'b', 'c'])
    @patch('show.open_show_from_file', side_effect=[Mock(id='x'), None, Mock(id='z')])
    def test_archive_file_not_opened(self, *args):
        '''Handles archived file open failing'''
        print(self.shortDescription())
        
        shows = show.get_archived_shows()
        self.assertEqual(len(shows.keys()), 2, 'Shows without files are not returned')
    

    @patch('os.listdir', return_value=['a'])
    @patch('show.open_show_from_file')
    def test_archive_file_custom_path(self, open_show_from_file, *args):
        '''Accepts a custom path to the show files directory'''
        print(self.shortDescription())
        
        show.get_archived_shows('custom/path')
        open_show_from_file.assert_called_with('custom/path/a')

    @patch('show.Show')
    @patch('utils.files.open_json_as_dict', return_value={'id': 1, 'title': 2, 'episodes': 3})
    def test_open_show_from_file(self, mock_open_json_as_dict, mock_Show):
        '''Creates a Show object if file returns data'''
        print(self.shortDescription())
        
        show.open_show_from_file('foo')
        mock_Show.assert_called()
    
    @patch('show.logger.warn')
    @patch('utils.files.open_json_as_dict', side_effect=OSError)
    def test_open_show_from_file_fails(self, mock_open_json_as_dict, *args):
        '''Handles failed file opens'''
        print(self.shortDescription())
        
        output = show.open_show_from_file('foo')
        self.assertTrue(output is None, 'Returns "None" if an exception occure')
        

if __name__ == '__main__':
    unittest.main()