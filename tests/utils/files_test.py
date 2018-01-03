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

    @patch('utils.files.open')
    @patch('ntpath.basename', return_value='file_name')
    @patch('utils.files.mkdir')
    @patch('ntpath.exists', return_value=False)
    def test_touch_new_file(self, exists, mkdir, basename, file_open):
        '''Creates file and folder(s) if the path does not exists'''
        print(self.shortDescription())
        path = 'foo/bar.baz'

        mock_file = Mock()
        file_open.return_value = mock_file
        output = uf.touch(path)
        self.assertTrue(output)
        mkdir.assert_called_once_with(path)
        file_open.assert_called_once_with(path, 'w')
        self.assertTrue(mock_file.close.called, 'Closes file handler')
    

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
        makedirs.assert_called_once_with('foo/bar')
        self.assertTrue(output)
    
    @patch('ntpath.exists', return_value=True)
    def test_mkdir_exists(self, exists):
        '''Returns False if the directory exists'''
        print(self.shortDescription())
        path = 'foo/bar/file.ext'
        output = uf.mkdir(path)
        self.assertFalse(output)
    
    @patch('json.dump')    
    @patch('utils.files.open')    
    def test_write_dict_as_json(self, file_open, json_dump):
        '''Writes dict as JSON file'''
        print(self.shortDescription())
        mock_file = Mock()
        file_open.return_value = mock_file
        obj = {'foo': 'bar'}
        path = 'baz.json'

        uf.write_dict_as_json(obj, path)

        file_open.assert_called_once_with(path, 'w')
        json_dump.assert_called_once_with(obj, mock_file)
        mock_file.close.assert_called_once()



if __name__ == '__main__':
    unittest.main()
