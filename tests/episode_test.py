import os
import sys
import unittest
import episode_fixtures as ef
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from episode import Episode

class TestEpisode(unittest.TestCase):  
  def test_set_operations(self):
    '''Supports set operations'''
    print(self.shortDescription())

    a = { Episode(ef.set_data[0]), Episode(ef.set_data[1]) }
    b = { Episode(ef.set_data[0]) }
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


if __name__ == '__main__':
  print('hi', __name__)
  unittest.main()