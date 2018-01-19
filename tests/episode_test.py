import os
import sys
import unittest
import episode_fixtures as ef
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from episode import Episode, parse_entry, audio_path_to_url

class TestEpisode(unittest.TestCase):  
    def test_set_operations(self):
        '''Supports set operations'''
        print(self.shortDescription())

        a = {Episode(ef.set_data[0]), Episode(ef.set_data[1])}
        b = {Episode(ef.set_data[0])}
        c = a - b
        self.assertEqual(next(iter(c)).id, ef.set_data[1]['id'])

    def test_equality(self):
        '''Equality is based on ids'''
        print(self.shortDescription())

        a = Episode(ef.equality_data[0])
        b = Episode(ef.equality_data[1])
        c = Episode(ef.equality_data[2])
        self.assertEqual(a, b)
        self.assertNotEqual(b, c)

    def test_object_reference(self):
        '''constructor dict is copied by value'''
        print(self.shortDescription())

        a = Episode(ef.objref_data)
        self.assertEqual(a.id, 999)
        ef.objref_data['id'] = 777
        self.assertEqual(a.id, 999)

    def test_immutability(self):
        '''Data properties are immutable'''
        print(self.shortDescription())

        a = Episode(ef.equality_data[0])
        self.assertRaises(AttributeError, lambda: ef.change_attr(a, 'id', 'new id'))
        self.assertRaises(AttributeError, lambda: ef.change_attr(a, 'title', 'new title'))
        self.assertRaises(AttributeError, lambda: ef.change_attr(a, 'web_page', 'new web_page'))
        self.assertRaises(AttributeError, lambda: ef.change_attr(a, 'description', 'new description'))
        self.assertRaises(AttributeError, lambda: ef.change_attr(a, 'video', 'new video'))
        self.assertRaises(AttributeError, lambda: ef.change_attr(a, 'thumbnail', 'new thumbnail'))
    
    def test_property_values(self):
        '''Properties set from dict'''
        print(self.shortDescription())

        e = Episode(ef.init_data)
        self.assertEqual(ef.init_data['id'], e.id)
        self.assertEqual(ef.init_data['title'], e.title)
        self.assertEqual(ef.init_data['web_page'], e.web_page)
        self.assertEqual(ef.init_data['description'], e.description)
        self.assertEqual(ef.init_data['thumbnail'], e.thumbnail)
        self.assertEqual(ef.init_data['video'], e.video)
        self.assertEqual(ef.init_data['audio_path'], e.audio_path)
        self.assertEqual(ef.init_data['date'], e.date)
        self.assertEqual(e.download_status, {})


    @patch('episode.change_ext', return_value='foo.mp3')
    def test_update_dl_status(self, change_ext):
        '''Sets download_status audio path'''
        print(self.shortDescription())

        e = Episode(ef.init_data)
        status_update = {'filename':'foo'}
        e.download_status = status_update
        self.assertEqual(e.download_status, status_update, 'Updates download_status property')
        change_ext.assert_called_once_with(status_update['filename'], '.mp3')
        self.assertEqual(e.audio_path, 'foo.mp3', 'Updates audio_path property')
        

    def test_parse_entry(self):
        '''Normalizes xmldict from feed'''
        print(self.shortDescription())

        entry = parse_entry(ef.xmldict)
        self.assertEqual(entry['id'], 'id')
        self.assertEqual(entry['title'], 'title')
        self.assertEqual(entry['web_page'], 'web_page')
        self.assertEqual(entry['description'], 'description')
        self.assertEqual(entry['thumbnail'], 'thumbnail')
        self.assertEqual(entry['video'], 'video')
        
    def test_download_finished(self):
        '''Reports if download is finished'''
        print(self.shortDescription())

        e = Episode(ef.init_no_audio_path)
        self.assertFalse(e.download_finished, 'False if status and audio path is not set')
        status_update = {'status': 'finished'}
        e.download_status = status_update
        self.assertTrue(e.download_finished, 'True if status is finished')
        
        e = Episode(ef.init_with_audio_path)
        self.assertTrue(e.download_finished, 'True if audio_path is set')

    @patch('episode.logger')
    @patch('os.rename')
    def test_archive_audio(self, rename, logger):
        '''Archive audio files'''
        print(self.shortDescription())

        e = Episode(ef.init_with_audio_path)
        dest = 'foo/bar.mp3'
        e.archive_audio(dest)
        rename.assert_called_once_with(ef.init_with_audio_path['audio_path'], dest)

        rename.side_effect = OSError('oops')
        e.archive_audio(dest)
        logger.exception.assert_called_once_with('oops')

    def test_to_dict(self):
        '''Converts to a dictionary'''
        print(self.shortDescription())

        e = Episode(ef.init_with_audio_path)
        output = e.to_dict()
        self.assertTrue(isinstance(output, dict))
        self.assertDictEqual(output, ef.init_with_audio_path)
    
    @patch('episode.file_and_parent', return_value=('file_name', 'parent'))
    def test_audio_path_url(self, file_and_parent):
        '''Converts a local audio path to url'''
        path = 'path'
        url_base = 'url_base/'
        self.assertEqual(
            audio_path_to_url(path, url_base),
            f'url_base/parent/file_name',
            'Concatenates url base with file and parent directory'
            )


if __name__ == '__main__':
  unittest.main()