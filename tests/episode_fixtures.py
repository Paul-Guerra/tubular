set_data = [
  {
    'id': 1,
    'title': 'title_1',
    'web_page': 'web_page_1',
    'description': 'description_1',
    'video': 'video_1',
    'thumbnail': 'thumbnail_1',
  },
  {
    'id': 2,
    'title': 'title_2',
    'web_page': 'web_page_2',
    'description': 'description_2',
    'video': 'video_2',
    'thumbnail': 'thumbnail_2',
  },
  {
    'id': 3,
    'title': 'title_3',
    'web_page': 'web_page_3',
    'description': 'description_3',
    'video': 'video_3',
    'thumbnail': 'thumbnail_3',
  },

  {
    'id': 4,
    'title': 'title_4',
    'web_page': 'web_page_4',
    'description': 'description_4',
    'video': 'video_4',
    'thumbnail': 'thumbnail_4',
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
  },
  {
    'id': 1,
    'title': 'title_2',
    'web_page': 'web_page_2',
    'description': 'description_2',
    'video': 'video_2',
    'thumbnail': 'thumbnail_2'
  }, 
  {
    'id': 3,
    'title': 'title_2',
    'web_page': 'web_page_2',
    'description': 'description_2',
    'video': 'video_2',
    'thumbnail': 'thumbnail_2'
  }, 
]

objref_data = {
    'id': 999,
    'title': 'objref_data_title_1',
    'web_page': 'objref_data_web_page_1',
    'description': 'objref_data_description_1',
    'video': 'objref_data_video_1',
    'thumbnail': 'objref_data_thumbnail_1',
  }

def change_attr(e, prop, value):
  setattr(e, prop, value)