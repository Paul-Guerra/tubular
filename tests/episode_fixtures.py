init_data = {
    'id': 1,
    'title': 'title_1',
    'web_page': 'web_page_1',
    'description': 'description_1',
    'video': 'video_1',
    'thumbnail': 'thumbnail_1',
    'date': 'the date',
    'audio_path': 'foo/bar/baz1.mp3'
}

init_no_audio_path = {
    'id': 1,
    'title': 'title_1',
    'web_page': 'web_page_1',
    'description': 'description_1',
    'video': 'video_1',
    'thumbnail': 'thumbnail_1',
    'date': 'the date'
}

init_with_audio_path = {
    'id': 1,
    'title': 'title_1',
    'web_page': 'web_page_1',
    'description': 'description_1',
    'video': 'video_1',
    'thumbnail': 'thumbnail_1',
    'date': 'the date',
    'audio_path': 'foo/bar/baz1.mp3'
}

set_data = [
  {
    'id': 1,
    'title': 'title_1',
    'web_page': 'web_page_1',
    'description': 'description_1',
    'video': 'video_1',
    'thumbnail': 'thumbnail_1',
    'date': 'the date',    
    'audio_path': 'foo/bar/baz1.mp3'
  },
  {
    'id': 2,
    'title': 'title_2',
    'web_page': 'web_page_2',
    'description': 'description_2',
    'video': 'video_2',
    'thumbnail': 'thumbnail_2',
    'date': 'the date',
    'audio_path': 'foo/bar/baz2.mp3'
  },
  {
    'id': 3,
    'title': 'title_3',
    'web_page': 'web_page_3',
    'description': 'description_3',
    'video': 'video_3',
    'thumbnail': 'thumbnail_3',
    'date': 'the date',
    'audio_path': 'foo/bar/baz3.mp3'
  },

  {
    'id': 4,
    'title': 'title_4',
    'web_page': 'web_page_4',
    'description': 'description_4',
    'video': 'video_4',
    'thumbnail': 'thumbnail_4',
    'date': 'the date',
    'audio_path': 'foo/bar/baz4.mp3'
  }
]

equality_data = [
  {
    'id': 1,
    'title': 'title_1',
    'web_page': 'web_page_1',
    'description': 'description_1',
    'video': 'video_1',
    'thumbnail': 'thumbnail_1',
    'date': 'the date',
    'audio_path': 'foo/bar/baz1.mp3'
  },
  {
    'id': 1,
    'title': 'title_2',
    'web_page': 'web_page_2',
    'description': 'description_2',
    'video': 'video_2',
    'thumbnail': 'thumbnail_2',
    'date': 'the date',
    'audio_path': 'foo/bar/baz2.mp3'
  }, 
  {
    'id': 3,
    'title': 'title_2',
    'web_page': 'web_page_2',
    'description': 'description_2',
    'video': 'video_2',
    'thumbnail': 'thumbnail_2',
    'date': 'the date',
    'audio_path': 'foo/bar/baz2.mp3'
  }, 
]

objref_data = {
    'id': 999,
    'title': 'objref_data_title_1',
    'web_page': 'objref_data_web_page_1',
    'description': 'objref_data_description_1',
    'video': 'objref_data_video_1',
    'thumbnail': 'objref_data_thumbnail_1',
    'date': 'the date',
    'audio_path': 'foo/bar/baz1.mp3'
}

xmldict = {
    'yt:videoId': 'id',
    'link': {'@href': 'web_page'},
    'updated': 'the date',
    'media:group': {
        'media:title': 'title',
        'media:description': 'description',
        'media:thumbnail': {'@url': 'thumbnail'},
        'media:content': {'@url': 'video'}
    }
}

def change_attr(e, prop, value):
  setattr(e, prop, value)
