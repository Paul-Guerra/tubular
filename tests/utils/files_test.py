import os
import sys
import unittest
from unittest.mock import patch, mock_open, Mock, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__ + '/../'))))
import utils.files as uf

class TestUtilsFiles(unittest.TestCase):  
    def test_change_ext(self):
        '''Changes file extension for a given path string '''
        print(self.shortDescription())
        self.assertEqual(uf.change_ext('/foo/bo.o/bar.baz', '.que'), '/foo/bo.o/bar.que')

    @patch('ntpath.exists', return_value=True)
    def test_touch_exists(self, exists):
        '''Does nothing if the path exists'''
        print(self.shortDescription())
        self.assertFalse(uf.touch('/foo/bar.baz'))

    @patch('ntpath.basename', return_value='file_name')
    @patch('utils.files.mkdir')
    @patch('ntpath.exists', return_value=False)
    def test_touch_new_file(self, exists, mkdir, basename):
        '''Creates file and folder(s) if the path does not exists'''
        print(self.shortDescription())
        path = 'foo/bar.baz'

        opener = mock_open()
        with patch('utils.files.open', opener) as mo:
            output = uf.touch(path)
            self.assertTrue(output)
            mkdir.assert_called_once_with(path)
            mo.assert_called_once_with(path, 'w')
            mo().close.assert_called_once()
    

    @patch('ntpath.basename', return_value='')
    @patch('utils.files.mkdir')
    @patch('ntpath.exists', return_value=False)
    def test_touch_no_file_name(self, exists, mkdir, basename):
        '''Doesnt create file if no file name is found in path'''
        print(self.shortDescription())
        self.shortDescription()
        path = 'foo/'
        with patch('utils.files.open', mock_open(), create=True) as mo:
            output = uf.touch(path)
            mo.assert_not_called()
            self.assertFalse(output)

    @patch('ntpath.dirname', return_value='foo/bar')
    @patch('os.makedirs')
    @patch('ntpath.exists', return_value=False)
    def test_mkdir(self, exists, makedirs, dirname):
        '''Create the folders if they do not exist'''
        print(self.shortDescription())
        path = 'foo/bar/file.ext'
        output = uf.mkdir(path)
        dirname.assert_called_once_with(path)
        makedirs.assert_called_once_with('foo/bar', exist_ok=True)
        self.assertTrue(output)

    @patch('ntpath.exists', return_value=True)
    def test_mkdir_exists(self, exists):
        '''Returns False if the directory exists'''
        print(self.shortDescription())
        path = 'foo/bar/file.ext'
        output = uf.mkdir(path)
        self.assertFalse(output)

    @patch('json.dump')
    def test_write_dict_as_json(self, json_dump):
        '''Writes dict as JSON file'''
        print(self.shortDescription())

        obj = {'foo': 'bar'}
        path = 'baz.json'

        opener = mock_open()
        with patch('utils.files.open', opener) as mo:
            uf.write_dict_as_json(obj, path)
            mo.assert_called_once_with(path, 'w')
            handle = mo()
            handle.close.assert_called_once()
            json_dump.assert_called_once_with(obj, handle)

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={'foo': 'bar'})
    def test_open_json_as_dict(self, json_load, path_exists):
        '''Open dict as JSON file'''
        print(self.shortDescription())

        path = 'baz.json'
        opener = mock_open()
        with patch('utils.files.open', opener) as mo:
            output = uf.open_json_as_dict(path)
            mo.assert_called_once_with(path, 'r')
            handle = mo()
            handle.close.assert_called_once()
            json_load.assert_called_once_with(handle)
            self.assertEqual(output, json_load.return_value, 'Returns dict from json.load')


    @patch('os.path.exists', return_value=False)
    def test_open_json_as_dict_bad_path(self, path_exists):
        '''Handles bad paths'''
        print(self.shortDescription())

        path = 'baz.json'
        opener = mock_open()
        with patch('utils.files.open', opener) as mo:
            output = uf.open_json_as_dict(path)
            self.assertFalse(output, 'Returns False if the path does not exist')


    @patch('os.path.isfile', return_value=True)
    def test_is_json_file(self, path_is_file):
        '''Detects JSON files from path'''
        print(self.shortDescription())

        json_path = 'foo/bar/baz.json'
        not_json_path = 'foo/bar/baz.yaml'
        self.assertTrue(uf.is_json_file(json_path), 'True if is file and name ends in ".json"')
        self.assertFalse(uf.is_json_file(not_json_path), 'False if extension is not ".json"')
        path_is_file.return_value = False
        self.assertFalse(uf.is_json_file(json_path), 'False if path does not point to file')

    @patch('ntpath.split', side_effect=[('folder', 'file_name'), ('_', 'parent')])
    def test_file_and_parent(self, split):
        result = uf.file_and_parent('path')
        self.assertTupleEqual(result, ('parent', 'file_name'))

if __name__ == '__main__':
    unittest.main()
